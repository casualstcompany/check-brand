from http import HTTPStatus

from api.v1.response_code import get_error_response
from api.v1.serialization.auth import AuthenticationSchema, GetNonceSchema
from api.v1.swag import account as swag
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.account import account_service
from services.jwt_generator import jwt
from services.web3 import web3_service

auth = Blueprint("auth_api", __name__)


@auth.route("/web3/nonce", methods=("GET",))
@swag_from(swag.get_nonce)
def get_nonce():
    # TODO: Как то криво, почему не прописал в путь
    public_address = request.args.get("public_address")

    if not public_address:
        return get_error_response.error(
            "public_address is not exist", status_code=HTTPStatus.BAD_REQUEST
        )

    public_address = public_address.lower()
    data = {"public_address": public_address}

    schema = GetNonceSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    if not web3_service.validate_public_address(data["public_address"]):
        return (
            jsonify(public_address=["Invalid public address."]),
            HTTPStatus.BAD_REQUEST,
        )
    nonce = account_service.get_nonce(data["public_address"])

    return jsonify(nonce=nonce), HTTPStatus.OK


@auth.route("/web3/login", methods=("POST",))
@swag_from(swag.authentication)
def authentication():
    data = request.json
    schema = AuthenticationSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return get_error_response.error_400(err.message)

    if not account_service.authentication(
        data["public_address"], data["signature"]
    ):
        return get_error_response.error(
            "authentication error", status_code=HTTPStatus.UNAUTHORIZED
        )
    account_service.add_login_history(
        data["public_address"], request.user_agent.string
    )
    # TODO потом разблокировать

    # account_service.change_nonce(data["public_address"])
    access_token, refresh_token = jwt.login(
        data["public_address"], request.user_agent.string
    )

    return (
        jsonify(access_token=access_token, refresh_token=refresh_token),
        HTTPStatus.OK,
    )


@auth.route("/refresh", methods=("POST",))
@jwt_required(refresh=True)
@swag_from(swag.refresh)
def refresh():
    public_address = get_jwt_identity()
    public_address = public_address.lower()
    authorization = request.headers.get("Authorization")
    old_refresh = authorization.split()[1]
    tokens = jwt.refresh(
        public_address, request.user_agent.string, old_refresh
    )
    if not tokens:
        return get_error_response.error(
            "token has been revoked", status_code=HTTPStatus.UNAUTHORIZED
        )
    return (
        jsonify(access_token=tokens[0], refresh_token=tokens[1]),
        HTTPStatus.OK,
    )


@auth.route("/logout", methods=("POST",))
@jwt_required()
@swag_from(swag.logout)
def logout():
    public_address = get_jwt_identity()
    public_address = public_address.lower()
    jti = get_jwt()["jti"]
    jwt.logout(public_address, request.user_agent.string, jti)
    return jsonify(msg="success logout")


@auth.route("/full_logout", methods=("POST",))
@jwt_required()
@swag_from(swag.full_logout)
def full_logout():
    public_address = get_jwt_identity()
    public_address = public_address.lower()
    jwt.full_logout(public_address)
    return jsonify(msg="success logout")
