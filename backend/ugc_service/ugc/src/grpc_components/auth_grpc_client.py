import logging
from http import HTTPStatus

import grpc
from google.protobuf.json_format import MessageToDict

from grpc_components.protobufs.auth_grpc_pb2 import AuthRequest
from grpc_components.protobufs.auth_grpc_pb2_grpc import AuthStub
from core import error
from core.config import get_settings as settings


channel = grpc.insecure_channel(f"{settings.GRPC.HOST}:{settings.GRPC.PORT}")
client = AuthStub(channel)
# TODO: переделать под общий формат base_grpc_client
# TODO: сделать через сертификат


async def get_auth_user(token):
    user_request = AuthRequest(access_key=token)

    try:
        user_response = client.GetUserRole(user_request)
    except grpc.RpcError as e:
        # TODO: оставить отлавливание (14 No connection) и поставить backoff
        logging.error(e.code())
        logging.error(e.details())

        if e.code() == grpc.StatusCode.UNAUTHENTICATED or e.code() == grpc.StatusCode.INVALID_ARGUMENT:

            detail = "token is not valid"
            if e.details() == "token expired":
                detail = "token expired"
            if e.details() == "token has been revoked":
                detail = "token has been revoked"

            raise error.BaseError(detail=detail, status_code=HTTPStatus.UNAUTHORIZED)

        raise error.BaseError(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    user_response = MessageToDict(user_response, preserving_proto_field_name=True)
    return user_response
