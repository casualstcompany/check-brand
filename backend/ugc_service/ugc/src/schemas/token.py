from typing import List
from uuid import UUID

from schemas.base import BaseSchema


class TokenListSchema(BaseSchema):
    tokens: List[UUID]
