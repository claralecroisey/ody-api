from flask import Blueprint, g, jsonify, request
from app.services.job_application import create_job_application
from security.guards import protected


jobs_bp = Blueprint("job_application", __name__)


@jobs_bp.route("/job-application", methods=["POST"])
@protected
def register_job_application():
    from app import app

    try:
        data = request.get_json()
        user_id = g.user_id
        create_job_application(user_id, data)

        return jsonify(message="Successfully created"), 201
    except Exception as e:
        app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400
