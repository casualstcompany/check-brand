from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from grpc_components.auth_grpc_client import get_auth_user
from core import error


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise error.BaseError(status_code=403, detail="invalid authentication")
            if not len(credentials.credentials.split()) == 1:
                raise error.BaseError(status_code=403, detail="invalid authentication")

            return await get_auth_user(credentials.credentials)
        else:
            raise error.BaseError(status_code=403, detail="invalid authorization code")
