from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import jwt_required

from app import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    from app.models import User

    users = User.query.all()
    return make_response([user.json() for user in users])


@user_bp.route("/users", methods=["POST"])
def create_user():
    from app.models import User

    try:
        data = request.get_json()
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "user created"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "error creating user"}), 500)
