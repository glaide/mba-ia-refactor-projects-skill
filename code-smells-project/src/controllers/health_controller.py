from flask import jsonify
from werkzeug.exceptions import HTTPException

from src.models import health_model


def health_check():
    health_model.ping()
    counts = health_model.get_counts()
    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": counts,
        "versao": "1.0.0",
    }), 200
