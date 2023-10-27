from flask import Blueprint
from flask_jwt_extended import jwt_required


user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    from app.models import User

    users = User.query.all()
    return [user.email for user in users]
