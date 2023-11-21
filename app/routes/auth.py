from flask import Blueprint, jsonify, request
from app.services.user import create_user_if_not_exists
from security.guards import extract_user_id
from app import basic_auth

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("", methods=["POST"])
@basic_auth.required
def register_user_if_not_exists():
    """
    Endpoint called by Auth0 to register new users in our DB
    (using a Post login Auth0 action)
    """
    from app import app

    try:
        data = request.get_json()
        user_id = extract_user_id(data["user_id"])
        create_user_if_not_exists(user_id)

        return jsonify(message="User is registered"), 200
    except Exception as e:
        app.logger.error(e)
        return jsonify(message="An unexpected error happend"), 400
