from flask import g, jsonify, request

from src.models import usuario_model
from src.services.auth_service import create_token, require_admin, require_auth


@require_admin
def listar():
    usuarios = usuario_model.get_all()
    return jsonify({"dados": usuarios, "sucesso": True}), 200


@require_auth
def buscar(usuario_id):
    if g.current_user.get("tipo") != "admin" and g.current_user.get("id") != usuario_id:
        return jsonify({"erro": "Acesso negado", "sucesso": False}), 403

    usuario = usuario_model.get_by_id(usuario_id)
    if usuario:
        return jsonify({"dados": usuario, "sucesso": True}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404


def criar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")
    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    usuario_id = usuario_model.create(nome, email, senha)
    return jsonify({"dados": {"id": usuario_id}, "sucesso": True}), 201


def login():
    dados = request.get_json()
    email = dados.get("email", "")
    senha = dados.get("senha", "")
    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = usuario_model.login(email, senha)
    if usuario:
        usuario["token"] = create_token(usuario)
        return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
    return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
