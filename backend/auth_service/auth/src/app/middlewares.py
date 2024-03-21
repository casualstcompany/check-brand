from extension import jwt
from flask import Flask, g, request
from utils.check_token import check_token_in_cache


def init_token_check(app: Flask):
    @app.before_request
    def is_valid_token():
        authorization = request.headers.get("Authorization")
        if authorization and len(authorization) == 2:
            g.access_token = authorization.split()[1]


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return check_token_in_cache(jwt_payload)
