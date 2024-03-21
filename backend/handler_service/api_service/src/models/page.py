from datetime import datetime
from typing import List

from models.base import BaseSchema, BaseListPage


class BasePageIn(BaseSchema):
    id: str
    name: str


class PageInCollection(BasePageIn):
    pass


class PageInAccount(BasePageIn):
    pass


class Page(BaseSchema):
    id: str
    hide: bool
    name: str
    number: int
    url: str
    banner: str = None
    title_1: str = None
    description: str = None
    title_2: str = None
    icon: str = None
    created_at: datetime
    updated_at: datetime

    class Meta:
        index = "page"


class PageDetail(Page):
    pass


class PageList(Page):
    # TODO: решить что выводить
    pass


class PageListPage(BaseListPage):
    results: List[PageList]

