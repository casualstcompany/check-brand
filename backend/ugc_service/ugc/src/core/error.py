from fastapi import HTTPException
import grpc


class UnavailableException(Exception):
    status = grpc.StatusCode.UNAVAILABLE
    code = grpc.StatusCode.UNAVAILABLE


class BaseError(HTTPException):
    pass
