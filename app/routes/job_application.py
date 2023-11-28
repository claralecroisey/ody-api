from uuid import UUID

from flask import Blueprint, current_app, g, jsonify, make_response, request

from app.services.job_application import (
    check_user_owns_job_application,
    create_job_application,
    delete_job_application,
    get_user_job_applications,
    update_job_application,
)
from security.guards import protected

jobs_bp = Blueprint("job_applications", __name__, url_prefix="/job-applications")


@jobs_bp.route("", methods=["GET"])
@protected
def get_user_applications():
    try:
        user_applications = get_user_job_applications(g.user_id)

        return (
            make_response([application.to_dict() for application in user_applications]),
            200,
        )
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400


@jobs_bp.route("", methods=["POST"])
@protected
def register_job_application():
    try:
        data = request.get_json()
        user_id = g.user_id
        create_job_application(user_id, data)

        return jsonify(message="Successfully created"), 201
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400


@jobs_bp.route("/<id>", methods=["PUT"])
@protected
def update_user_job_application(id: UUID):
    try:
        user_owns_job_application = check_user_owns_job_application(
            job_id=id, user_id=g.user_id
        )
        if not user_owns_job_application:
            return jsonify(message="Job application not found"), 404

        data = request.get_json()
        updated_job = update_job_application(job_id=id, data=data)

        return (
            jsonify(updated_job=updated_job.to_dict() if updated_job else None),
            200,
        )
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400


@jobs_bp.route("/<id>", methods=["DELETE"])
@protected
def delete_user_job_application(id: UUID):
    try:
        user_owns_job_application = check_user_owns_job_application(
            job_id=id, user_id=g.user_id
        )
        if not user_owns_job_application:
            return jsonify(message="Job application not found"), 404

        delete_job_application(job_id=id)

        return (
            jsonify(message=f"Successfully deleted job application with id {id}"),
            200,
        )
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(message=f"An unexpected error happend {str(e)}"), 400
