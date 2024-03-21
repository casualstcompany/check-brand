from http import HTTPStatus

from api.v1.response_code import InvalidAPIUsage
from flask import json, jsonify


def handle_exception(e):
    error = InvalidAPIUsage(
        "Something went wrong", status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )
    return jsonify(error.to_dict()), error.status_code
