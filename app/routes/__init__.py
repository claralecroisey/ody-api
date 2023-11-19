from .job_listing import jobs_bp


def register_routes(app):
    app.register_blueprint(jobs_bp)
