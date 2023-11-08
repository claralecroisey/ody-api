from flask import Blueprint, jsonify


jobs_bp = Blueprint("job_listing", __name__)


@jobs_bp.route("/jobs", methods=["GET"])
def get_job_listings():
    return jsonify(
        jobs=[
            {
                "title": "Software Engineer",
                "company": "Google",
            },
            {
                "title": "Software Engineer",
                "company": "Facebook",
            },
            {
                "title": "Software Engineer",
                "company": "Apple",
            },
            {
                "title": "Software Engineer",
                "company": "Microsoft",
            },
            {
                "title": "Software Engineer",
                "company": "Amazon",
            },
        ]
    )
