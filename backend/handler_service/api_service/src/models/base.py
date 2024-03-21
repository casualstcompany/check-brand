from typing import List

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True

    class Meta:
        index = None

    @classmethod
    def get_class_meta(cls):
        return cls.Meta


class BaseListPage(BaseSchema):
    results: List[BaseSchema]
    count: int
    total_pages: int
    page: int
    page_size: int
