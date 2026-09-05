from functools import wraps

from flask import g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from src.config.settings import SECRET_KEY, TOKEN_MAX_AGE

_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="auth-token")


def create_token(user):
    return _serializer.dumps({"id": user["id"], "tipo": user["tipo"]})


def verify_token(token):
    try:
        return _serializer.loads(token, max_age=TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.removeprefix("Bearer ").strip()
        if not token:
            return jsonify({"erro": "Token não fornecido", "sucesso": False}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({"erro": "Token inválido ou expirado", "sucesso": False}), 401

        g.current_user = payload
        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        if g.current_user.get("tipo") != "admin":
            return jsonify({"erro": "Acesso negado", "sucesso": False}), 403
        return f(*args, **kwargs)

    return decorated
