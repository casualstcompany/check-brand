from schemes.base import BaseSchema


class ErrorResponseSchema(BaseSchema):
    data: str
    status: str
