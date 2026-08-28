from werkzeug.security import generate_password_hash, check_password_hash
from src.database import get_db


def _safe_user(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }


def get_all():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [_safe_user(row) for row in cursor.fetchall()]


def get_by_id(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    return _safe_user(row) if row else None


def create(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    hashed = generate_password_hash(senha)
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, hashed, tipo),
    )
    db.commit()
    return cursor.lastrowid


def login(email, senha):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row and check_password_hash(row["senha"], senha):
        return _safe_user(row)
    return None
