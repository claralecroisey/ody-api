from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.extensions import basic_auth, db, migrate
from app.routes import register_routes
from security.auth0_service import auth0_service
from utils import safe_get_env_var


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)


def create_app():
    load_dotenv()

    client_url = safe_get_env_var("CLIENT_URL")
    db_url = safe_get_env_var("DATABASE_URL")
    auth0_audience = safe_get_env_var("AUTH0_AUDIENCE")
    auth0_domain = safe_get_env_var("AUTH0_DOMAIN")
    basic_auth_username = safe_get_env_var("BASIC_AUTH_USERNAME")
    basic_auth_password = safe_get_env_var("BASIC_AUTH_PASSWORD")

    app = Flask(__name__)
    CORS(app, origins=[client_url], supports_credentials=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["CORS_HEADERS"] = "Content-Type"

    auth0_service.initialize(auth0_domain, auth0_audience)
    app.config["BASIC_AUTH_USERNAME"] = basic_auth_username
    app.config["BASIC_AUTH_PASSWORD"] = basic_auth_password

    register_extensions(app)
    register_routes(app)

    return app


app = create_app()
