from flask import Flask

from flask_cors import CORS

from app.extensions import db, migrate
from app.routes import register_routes

from dotenv import load_dotenv
from security.auth0_service import auth0_service

from utils import safe_get_env_var


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def create_app():
    load_dotenv()

    client_url = safe_get_env_var("CLIENT_URL")
    db_url = safe_get_env_var("DATABASE_URL")
    auth0_audience = safe_get_env_var("AUTH0_AUDIENCE")
    auth0_domain = safe_get_env_var("AUTH0_DOMAIN")

    _app = Flask(__name__)
    CORS(_app, origins=[client_url], supports_credentials=True)
    _app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    _app.config["CORS_HEADERS"] = "Content-Type"

    auth0_service.initialize(auth0_domain, auth0_audience)

    register_extensions(_app)
    register_routes(_app)

    return _app


app = create_app()
