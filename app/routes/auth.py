from flask import Blueprint, app, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


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


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).one_or_none()

    if user is not None and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=email)
        return jsonify(message="Login successful", access_token=access_token)
    else:
        return jsonify(message="Login failed"), 401
