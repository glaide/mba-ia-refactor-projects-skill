from datetime import timedelta

from flask import jsonify
from sqlalchemy import case, func
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from services.auth_service import require_manager_or_admin
from utils.datetime_utils import utc_now


@require_manager_or_admin
def summary_report():
    total_tasks = Task.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()

    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    now = utc_now()
    overdue_tasks = Task.query.filter(
        Task.due_date < now,
        Task.status.notin_(['done', 'cancelled']),
    ).all()

    overdue_list = [
        {
            'id': t.id,
            'title': t.title,
            'due_date': str(t.due_date),
            'days_overdue': (now - t.due_date).days,
        }
        for t in overdue_tasks
    ]

    seven_days_ago = now - timedelta(days=7)
    recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
    recent_done = Task.query.filter(
        Task.status == 'done',
        Task.updated_at >= seven_days_ago,
    ).count()

    user_stats_rows = (
        db.session.query(
            User.id,
            User.name,
            func.count(Task.id).label('total_tasks'),
            func.sum(case((Task.status == 'done', 1), else_=0)).label('completed_tasks'),
        )
        .outerjoin(Task, Task.user_id == User.id)
        .group_by(User.id, User.name)
        .all()
    )

    user_stats = [
        {
            'user_id': row.id,
            'user_name': row.name,
            'total_tasks': row.total_tasks,
            'completed_tasks': int(row.completed_tasks or 0),
            'completion_rate': round(
                (int(row.completed_tasks or 0) / row.total_tasks) * 100, 2
            ) if row.total_tasks > 0 else 0,
        }
        for row in user_stats_rows
    ]

    report = {
        'generated_at': str(now),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': total_users,
            'total_categories': total_categories,
        },
        'tasks_by_status': {
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
        },
        'tasks_by_priority': {
            'critical': Task.query.filter_by(priority=1).count(),
            'high': Task.query.filter_by(priority=2).count(),
            'medium': Task.query.filter_by(priority=3).count(),
            'low': Task.query.filter_by(priority=4).count(),
            'minimal': Task.query.filter_by(priority=5).count(),
        },
        'overdue': {
            'count': len(overdue_list),
            'tasks': overdue_list,
        },
        'recent_activity': {
            'tasks_created_last_7_days': recent_tasks,
            'tasks_completed_last_7_days': recent_done,
        },
        'user_productivity': user_stats,
    }
    return jsonify(report), 200


@require_manager_or_admin
def user_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    tasks = Task.query.filter_by(user_id=user_id).all()
    total = len(tasks)
    done = sum(1 for t in tasks if t.status == 'done')
    pending = sum(1 for t in tasks if t.status == 'pending')
    in_progress = sum(1 for t in tasks if t.status == 'in_progress')
    cancelled = sum(1 for t in tasks if t.status == 'cancelled')
    overdue = sum(1 for t in tasks if t.is_overdue())
    high_priority = sum(1 for t in tasks if t.priority <= 2)

    return jsonify({
        'user': {'id': user.id, 'name': user.name, 'email': user.email},
        'statistics': {
            'total_tasks': total,
            'done': done,
            'pending': pending,
            'in_progress': in_progress,
            'cancelled': cancelled,
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        },
    }), 200
