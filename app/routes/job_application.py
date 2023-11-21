from flask import Blueprint, g, jsonify, make_response, request

from app.services.job_application import (
    create_job_application,
    get_user_job_applications,
)
from security.guards import protected

jobs_bp = Blueprint("job_applications", __name__, url_prefix="/job-applications")


@jobs_bp.route("", methods=["POST"])
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


@jobs_bp.route("", methods=["GET"])
@protected
def get_user_applications():
    from app import app

    try:
        user_applications = get_user_job_applications(g.user_id)

        return (
            make_response([application.to_dict() for application in user_applications]),
            200,
        )
    except Exception as e:
        app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400
