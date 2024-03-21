from typing import Optional

from schemes.base import BaseSchema


class Profile(BaseSchema):
    public_address: Optional[str]
    username: Optional[str]
