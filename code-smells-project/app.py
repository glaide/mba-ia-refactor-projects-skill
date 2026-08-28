from flask import Flask
from flask_cors import CORS
from src.config.settings import SECRET_KEY, DEBUG, HOST, PORT
from src.database import get_db
from src.views.routes import register_routes
from src.middlewares.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    CORS(app)
    register_routes(app)
    register_error_handlers(app)
    get_db()
    return app


app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://localhost:{PORT}")
    print("=" * 50)
    app.run(host=HOST, port=PORT, debug=DEBUG)
