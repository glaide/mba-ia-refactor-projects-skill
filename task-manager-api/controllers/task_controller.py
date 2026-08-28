from datetime import datetime
from sqlalchemy.orm import joinedload
from flask import request, jsonify
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from services.notification_service import NotificationService

notifier = NotificationService()
VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']


def _task_with_relations(task):
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    data['user_name'] = task.user.name if task.user else None
    data['category_name'] = task.category.name if task.category else None
    return data


def list_tasks():
    tasks = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).all()
    return jsonify([_task_with_relations(t) for t in tasks]), 200


def get_task(task_id):
    task = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
    return jsonify(_task_with_relations(task)), 200


def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    title = data.get('title')
    if not title or len(title) < 3 or len(title) > 200:
        return jsonify({'error': 'Título inválido (3-200 caracteres)'}), 400

    status = data.get('status', 'pending')
    priority = data.get('priority', 3)
    if status not in VALID_STATUSES:
        return jsonify({'error': 'Status inválido'}), 400
    if priority < 1 or priority > 5:
        return jsonify({'error': 'Prioridade deve ser entre 1 e 5'}), 400

    user_id = data.get('user_id')
    category_id = data.get('category_id')
    if user_id and not User.query.get(user_id):
        return jsonify({'error': 'Usuário não encontrado'}), 404
    if category_id and not Category.query.get(category_id):
        return jsonify({'error': 'Categoria não encontrada'}), 404

    task = Task(
        title=title,
        description=data.get('description', ''),
        status=status,
        priority=priority,
        user_id=user_id,
        category_id=category_id,
    )

    due_date = data.get('due_date')
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

    tags = data.get('tags')
    if tags:
        task.tags = ','.join(tags) if isinstance(tags, list) else tags

    db.session.add(task)
    db.session.commit()

    if user_id:
        user = User.query.get(user_id)
        if user:
            notifier.notify_task_assigned(user, task)

    return jsonify(task.to_dict()), 201


def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if 'title' in data:
        if len(data['title']) < 3 or len(data['title']) > 200:
            return jsonify({'error': 'Título inválido'}), 400
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({'error': 'Status inválido'}), 400
        task.status = data['status']
    if 'priority' in data:
        if data['priority'] < 1 or data['priority'] > 5:
            return jsonify({'error': 'Prioridade inválida'}), 400
        task.priority = data['priority']
    if 'user_id' in data:
        task.user_id = data['user_id']
    if 'category_id' in data:
        task.category_id = data['category_id']
    if 'due_date' in data:
        if data['due_date']:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        else:
            task.due_date = None
    if 'tags' in data:
        task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict()), 200


def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deletada com sucesso'}), 200


def search_tasks():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')

    tasks = Task.query
    if query:
        tasks = tasks.filter(
            db.or_(
                Task.title.like(f'%{query}%'),
                Task.description.like(f'%{query}%'),
            )
        )
    if status:
        tasks = tasks.filter(Task.status == status)
    if priority:
        tasks = tasks.filter(Task.priority == int(priority))
    if user_id:
        tasks = tasks.filter(Task.user_id == int(user_id))

    return jsonify([t.to_dict() for t in tasks.all()]), 200


def task_stats():
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    overdue_count = Task.query.filter(
        Task.due_date < datetime.utcnow(),
        Task.status.notin_(['done', 'cancelled']),
    ).count()

    return jsonify({
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'cancelled': cancelled,
        'overdue': overdue_count,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
    }), 200
