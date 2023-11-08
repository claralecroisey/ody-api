from flask import Blueprint, jsonify

from security.guards import protected


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/test", methods=["GET"])
@protected
def test():
    return jsonify(message="Hello world"), 200
