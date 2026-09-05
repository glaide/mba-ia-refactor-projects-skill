from flask import Flask
from flask_cors import CORS
from database import db
from config.settings import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, HOST, PORT
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.report_routes import report_bp
from routes.category_routes import category_bp
from middlewares.error_handler import register_error_handlers
from utils.datetime_utils import utc_now


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG

    CORS(app)
    db.init_app(app)

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(category_bp)
    register_error_handlers(app)

    @app.route('/health')
    def health():
        return {'status': 'ok', 'timestamp': str(utc_now())}

    @app.route('/')
    def index():
        return {'message': 'Task Manager API', 'version': '1.0'}

    return app


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
