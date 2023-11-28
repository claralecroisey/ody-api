import os

from flask import Flask
from flask_cors import CORS

from app.extensions import basic_auth, db, migrate
from app.routes import register_routes
from config import DevConfig, ProdConfig
from security.auth0_service import auth0_service


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)


def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV")

    if env == "production":
        app.config.from_object(ProdConfig)
    elif env == "development":
        app.config.from_object(DevConfig)

    CORS(app, origins=[app.config["CLIENT_URL"]], supports_credentials=True)
    auth0_service.initialize(app.config["AUTH0_DOMAIN"], app.config["AUTH0_AUDIENCE"])

    register_extensions(app)
    register_routes(app)

    return app


app = create_app()
