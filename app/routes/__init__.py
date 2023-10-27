from .auth import auth_bp
from .user import user_bp


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
