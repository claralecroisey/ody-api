from functools import wraps
from http import HTTPStatus

from flask import request, g

from security.auth0_service import auth0_service
from utils import json_abort

unauthorized_error = {"message": "Requires authentication"}

invalid_request_error = {
    "error": "invalid_request",
    "error_description": "Authorization header value must follow this format: Bearer access-token",
    "message": "Requires authentication",
}


def get_bearer_token_from_request():
    authorization_header = request.headers.get("Authorization", None)

    if not authorization_header:
        json_abort(HTTPStatus.UNAUTHORIZED, unauthorized_error)
        return

    authorization_header_elements = authorization_header.split()

    if len(authorization_header_elements) != 2:
        json_abort(HTTPStatus.BAD_REQUEST, invalid_request_error)
        return

    auth_scheme = authorization_header_elements[0]
    bearer_token = authorization_header_elements[1]

    if not (auth_scheme and auth_scheme.lower() == "bearer"):
        json_abort(HTTPStatus.UNAUTHORIZED, unauthorized_error)
        return

    if not bearer_token:
        json_abort(HTTPStatus.UNAUTHORIZED, unauthorized_error)
        return

    return bearer_token


def protected(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        token = get_bearer_token_from_request()
        claims: dict = auth0_service.validate_jwt(token)

        sub_claim = claims.get("sub")
        user_id = extract_user_id(sub_claim)

        g.user_id = user_id

        return function(*args, **kwargs)

    return decorator


def extract_user_id(sub_claim: str):
    # Assuming 'sub' is in the format 'google-oauth2|0000000000000000000'
    if sub_claim:
        parts = sub_claim.split("|")
        if len(parts) == 2:
            return parts[1]

    return None
