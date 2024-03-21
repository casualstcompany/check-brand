from typing import Optional
from uuid import UUID

from schemas.base import BaseSchema


class AdminCollectionSchema(BaseSchema):
    id: UUID
    name: str
    logo: str
    status: str


class AdminTokenSchema(BaseSchema):
    id: UUID
    status_price: str
    price: float
    status: str
    collection: str
    name: str
    file_1: Optional[str]
    mint: bool = False

