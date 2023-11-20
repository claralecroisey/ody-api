from .job_application import jobs_bp


def register_routes(app):
    app.register_blueprint(jobs_bp)
