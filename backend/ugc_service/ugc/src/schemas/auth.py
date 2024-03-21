from typing import List

from schemas.base import BaseSchema


class User(BaseSchema):
    user_wallet: str
    user_role: List[str]
