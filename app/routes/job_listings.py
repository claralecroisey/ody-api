from flask import Blueprint
from flask_jwt_extended import jwt_required


jobs_bp = Blueprint("job_listing", __name__)


@jobs_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_job_listings():
    return []
