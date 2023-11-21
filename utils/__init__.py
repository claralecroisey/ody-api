from os import environ

from flask import abort, jsonify


def safe_get_env_var(key):
    try:
        return environ[key]
    except KeyError:
        raise NameError(f"Missing {key} environment variable.")


def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)
