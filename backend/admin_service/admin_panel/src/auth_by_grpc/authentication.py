from rest_framework_simplejwt.authentication import (
    AuthenticationFailed,
    InvalidToken,
    JWTAuthentication,
    _,
    api_settings,
)

from auth_by_grpc import message as msg
from auth_by_grpc.grpc_client import get_auth_user


class JWTGRPCUserAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Returns a stateless user object which is backed by the given validated
        token.
        """
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(msg.ERROR_401_TOKEN_NOT_VALID)
        return api_settings.TOKEN_USER_CLASS(validated_token)

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        validated_token = get_auth_user(raw_token)
        if not validated_token:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found"
            )
        return validated_token
