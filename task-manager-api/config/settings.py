import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///tasks.db")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))
