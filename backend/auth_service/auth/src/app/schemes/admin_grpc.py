from uuid import UUID

from schemes.base import BaseSchema


class AdminCollectionSchema(BaseSchema):
    account: UUID
