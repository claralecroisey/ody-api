from flask import Flask
import os

from app.extensions import db, migrate, jwt
from app.routes import register_routes

from dotenv import load_dotenv


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def create_app():
    load_dotenv()

    _app = Flask(__name__)
    _app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    _app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    register_extensions(_app)
    register_routes(_app)

    return _app


app = create_app()
