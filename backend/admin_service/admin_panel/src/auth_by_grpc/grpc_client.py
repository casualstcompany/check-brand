from http import HTTPStatus

import grpc
from google.protobuf.json_format import MessageToDict
from rest_framework.exceptions import AuthenticationFailed

from auth_by_grpc.protobufs.auth_grpc_pb2 import AuthRequest
from auth_by_grpc.protobufs.auth_grpc_pb2_grpc import AuthStub
from auth_by_grpc.settings import grpc_settings

channel = grpc.insecure_channel(
    f"{grpc_settings.HOST_GRPC}:{grpc_settings.PORT_GRPC}"
)
client = AuthStub(channel)


def get_auth_user(token):
    user_request = AuthRequest(access_key=token)

    try:
        user_response = client.GetUserRole(user_request)
    except grpc.RpcError as e:
        if (
            e.code() == grpc.StatusCode.UNAUTHENTICATED
            or e.code() == grpc.StatusCode.INVALID_ARGUMENT
        ):
            detail = "token is not valid"
            if e.details() == "token expired":
                detail = "token expired"
            if e.details() == "token has been revoked":
                detail = "token has been revoked"

            raise AuthenticationFailed(
                detail=detail, code=HTTPStatus.UNAUTHORIZED
            )

        raise AuthenticationFailed(code=HTTPStatus.INTERNAL_SERVER_ERROR)

    user_response = MessageToDict(
        user_response, preserving_proto_field_name=True
    )
    return user_response
