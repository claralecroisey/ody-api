from .auth import auth_bp
from .job_listing import jobs_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
