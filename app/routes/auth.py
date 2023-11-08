import os
from flask import Blueprint, app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/test", methods=["GET"])
@jwt_required()
def test():
    return jsonify(message="test"), 200


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        user = User.query.filter_by(email=email).one_or_none()

        if user is not None:
            return jsonify(message="Registration failed"), 401

        hashed_password = generate_password_hash(password)
        user = User(email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="user created"), 201
    except Exception as e:
        app.logger.error(e)
        return jsonify(message="Registration failed"), 401


@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).one_or_none()

    if user is not None and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=email)
        res = jsonify(
            message="Login successful",
            access_token=access_token,
            expires_in=os.environ.get("TOKEN_EXPIRATION_TIME"),
        )
        set_access_cookies(res, access_token)
        return res, 200
    else:
        return jsonify(message="Login failed"), 401
