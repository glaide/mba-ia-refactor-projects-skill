from flask import g, request, jsonify
from sqlalchemy.orm import joinedload
from database import db
from models.user import User
from models.task import Task
from services.auth_service import create_token, require_admin, require_auth, verify_token
from utils.helpers import MIN_PASSWORD_LENGTH, VALID_ROLES, validate_email


def _can_access_user(user_id):
    current = g.current_user
    return current.get('role') == 'admin' or current.get('id') == user_id


@require_admin
def list_users():
    users = User.query.options(joinedload(User.tasks)).all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'active': u.active,
            'created_at': str(u.created_at),
            'task_count': len(u.tasks),
        }
        for u in users
    ]), 200


@require_auth
def get_user(user_id):
    if not _can_access_user(user_id):
        return jsonify({'error': 'Acesso negado'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    data = user.to_dict()
    data['tasks'] = [t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]
    return jsonify(data), 200


def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400
    if not validate_email(email):
        return jsonify({'error': 'Email inválido'}), 400
    if len(password) < MIN_PASSWORD_LENGTH:
        return jsonify({'error': f'Senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado'}), 409

    role = 'user'
    header = request.headers.get("Authorization", "")
    token = header.removeprefix("Bearer ").strip()
    if token:
        payload = verify_token(token)
        if payload and payload.get('role') == 'admin':
            requested_role = data.get('role', 'user')
            if requested_role in VALID_ROLES:
                role = requested_role

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@require_auth
def update_user(user_id):
    if not _can_access_user(user_id):
        return jsonify({'error': 'Acesso negado'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email já cadastrado'}), 409
        user.email = data['email']
    if 'password' in data:
        if len(data['password']) < MIN_PASSWORD_LENGTH:
            return jsonify({'error': f'Senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres'}), 400
        user.set_password(data['password'])
    if 'role' in data:
        if g.current_user.get('role') != 'admin':
            return jsonify({'error': 'Apenas administradores podem alterar roles'}), 403
        if data['role'] not in VALID_ROLES:
            return jsonify({'error': 'Role inválido'}), 400
        user.role = data['role']
    if 'active' in data:
        if g.current_user.get('role') != 'admin':
            return jsonify({'error': 'Apenas administradores podem alterar status ativo'}), 403
        user.active = data['active']

    db.session.commit()
    return jsonify(user.to_dict()), 200


@require_admin
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    try:
        Task.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar usuário'}), 500

    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@require_auth
def get_user_tasks(user_id):
    if not _can_access_user(user_id):
        return jsonify({'error': 'Acesso negado'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([
        {**t.to_dict(), 'overdue': t.is_overdue()}
        for t in tasks
    ]), 200


def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    if not user.active:
        return jsonify({'error': 'Usuário inativo'}), 403

    user_data = user.to_dict()
    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user_data,
        'token': create_token(user_data),
    }), 200
