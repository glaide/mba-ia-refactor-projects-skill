from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"erro": "Método não permitido"}), 405

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"erro": error.description or "Erro na requisição"}), error.code

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(error)
        return jsonify({"erro": "Erro interno do servidor"}), 500
