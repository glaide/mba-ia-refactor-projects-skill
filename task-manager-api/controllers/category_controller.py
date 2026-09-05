from flask import request, jsonify
from sqlalchemy import func
from database import db
from models.category import Category
from models.task import Task
from services.auth_service import require_admin, require_auth
from utils.helpers import DEFAULT_COLOR, is_valid_color


@require_auth
def get_categories():
    rows = (
        db.session.query(Category, func.count(Task.id).label('task_count'))
        .outerjoin(Task, Task.category_id == Category.id)
        .group_by(Category.id)
        .all()
    )
    return jsonify([
        {**category.to_dict(), 'task_count': task_count}
        for category, task_count in rows
    ]), 200


@require_admin
def create_category():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400

    color = data.get('color', DEFAULT_COLOR)
    if not is_valid_color(color):
        return jsonify({'error': 'Cor inválida. Use formato #RRGGBB'}), 400

    category = Category(
        name=data['name'],
        description=data.get('description', ''),
        color=color,
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@require_admin
def update_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if 'name' in data:
        cat.name = data['name']
    if 'description' in data:
        cat.description = data['description']
    if 'color' in data:
        if not is_valid_color(data['color']):
            return jsonify({'error': 'Cor inválida. Use formato #RRGGBB'}), 400
        cat.color = data['color']

    db.session.commit()
    return jsonify(cat.to_dict()), 200


@require_admin
def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    try:
        Task.query.filter_by(category_id=cat_id).update({'category_id': None})
        db.session.delete(cat)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar categoria'}), 500

    return jsonify({'message': 'Categoria deletada'}), 200
