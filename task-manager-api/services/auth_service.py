from functools import wraps

from flask import g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from config.settings import SECRET_KEY, TOKEN_MAX_AGE

_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="auth-token")


def create_token(user):
    return _serializer.dumps({"id": user["id"], "role": user["role"]})


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
            return jsonify({"error": "Token não fornecido"}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        g.current_user = payload
        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        if g.current_user.get("role") != "admin":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)

    return decorated


def require_manager_or_admin(f):
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        if g.current_user.get("role") not in ("admin", "manager"):
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)

    return decorated
