import grpc
from components.protobufs import auth_grpc_pb2, auth_grpc_pb2_grpc
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError, exceptions
from services.user import user_service
from utils.check_token import check_token_in_cache


class Auth(auth_grpc_pb2_grpc.AuthServicer):
    def __init__(self, app):
        self.flask_app = app

    def GetUserRole(self, request, context):
        with self.flask_app.app_context():
            token = self.validate_token(context, request.access_key)

            if not token:
                return auth_grpc_pb2.AuthResponse(
                    user_role="", user_id="", user_wallet="", email=""
                )

            public_address = token.get("sub")
            user = user_service.get_by_public_address(
                public_address=public_address
            )

            user_id = user.public_address
            if user.profile[0].email_verified:
                email = user.profile[0].email
            else:
                email = ""
            user_wallet = user.public_address
            roles = [role.name for role in user.roles]

            return auth_grpc_pb2.AuthResponse(
                user_role=roles,
                user_id=user_id,
                user_wallet=user_wallet,
                email=email,
            )

    def validate_token(self, context, token):
        if not token:
            self.error(
                context, grpc.StatusCode.INVALID_ARGUMENT, "token is not valid"
            )
        try:
            token_info = decode_token(token)
        except exceptions.InvalidSignatureError:
            self.error(
                context, grpc.StatusCode.INVALID_ARGUMENT, "token is not valid"
            )
            return False
        except ExpiredSignatureError:
            self.error(
                context, grpc.StatusCode.UNAUTHENTICATED, "token expired"
            )
            return False

        if check_token_in_cache(token_info):
            self.error(
                context,
                grpc.StatusCode.UNAUTHENTICATED,
                "token has been revoked",
            )

        if token_info["type"] != "access":
            self.error(
                context, grpc.StatusCode.INVALID_ARGUMENT, "token is not valid"
            )

        return token_info

    def error(self, context, status, detail):
        context.set_code(status)
        context.set_details(detail)
