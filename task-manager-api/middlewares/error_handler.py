from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({'error': 'Recurso não encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({'error': 'Erro interno do servidor'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(error)
        return jsonify({'error': 'Erro interno do servidor'}), 500
