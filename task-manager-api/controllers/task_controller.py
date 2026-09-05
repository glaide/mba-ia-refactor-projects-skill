from sqlalchemy.orm import joinedload
from flask import request, jsonify
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from services.auth_service import require_auth
from services.notification_service import NotificationService
from utils.datetime_utils import utc_now
from utils.helpers import DEFAULT_PRIORITY, process_task_data

notifier = NotificationService()


def _task_with_relations(task):
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    data['user_name'] = task.user.name if task.user else None
    data['category_name'] = task.category.name if task.category else None
    return data


@require_auth
def list_tasks():
    tasks = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).all()
    return jsonify([_task_with_relations(t) for t in tasks]), 200


@require_auth
def get_task(task_id):
    task = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    ).get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
    return jsonify(_task_with_relations(task)), 200


@require_auth
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if not data.get('title'):
        return jsonify({'error': 'Título é obrigatório'}), 400

    processed, error = process_task_data(data)
    if error:
        return jsonify({'error': error}), 400

    user_id = data.get('user_id')
    category_id = data.get('category_id')
    if user_id and not User.query.get(user_id):
        return jsonify({'error': 'Usuário não encontrado'}), 404
    if category_id and not Category.query.get(category_id):
        return jsonify({'error': 'Categoria não encontrada'}), 404

    task = Task(
        title=processed.get('title', data['title']),
        description=processed.get('description', data.get('description', '')),
        status=processed.get('status', data.get('status', 'pending')),
        priority=processed.get('priority', data.get('priority', DEFAULT_PRIORITY)),
        user_id=user_id,
        category_id=category_id,
    )

    if 'due_date' in processed:
        task.due_date = processed['due_date']
    if 'tags' in processed:
        task.tags = processed['tags']

    db.session.add(task)
    db.session.commit()

    if user_id:
        user = User.query.get(user_id)
        if user:
            notifier.notify_task_assigned(user, task)

    return jsonify(task.to_dict()), 201


@require_auth
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    processed, error = process_task_data(data)
    if error:
        return jsonify({'error': error}), 400

    for field in ('title', 'description', 'status', 'priority', 'due_date', 'tags'):
        if field in processed:
            setattr(task, field, processed[field])

    if 'user_id' in data:
        task.user_id = data['user_id']
    if 'category_id' in data:
        task.category_id = data['category_id']

    task.updated_at = utc_now()
    db.session.commit()
    return jsonify(task.to_dict()), 200


@require_auth
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deletada com sucesso'}), 200


@require_auth
def search_tasks():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')

    tasks = Task.query.options(
        joinedload(Task.user),
        joinedload(Task.category),
    )
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

    return jsonify([_task_with_relations(t) for t in tasks.all()]), 200


@require_auth
def task_stats():
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    overdue_count = Task.query.filter(
        Task.due_date < utc_now(),
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
