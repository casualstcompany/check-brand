from typing import Union
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True


class BaseUUIDSchema(BaseSchema):
    id: Union[str, UUID]
