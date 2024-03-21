from datetime import datetime
from typing import List

from models.base import BaseSchema, BaseListPage
from models.enum import TokenTypeEnum
from models.page import PageInAccount


class BaseAccountIn(BaseSchema):
    id: str
    name: str


class AccountInCollection(BaseAccountIn):
    pass


class Account(BaseSchema):
    id: str
    hide: bool
    link_opensea: str = None
    link_discord: str = None
    link_instagram: str = None
    link_medium: str = None
    link_twitter: str = None
    type: TokenTypeEnum
    logo: str = None
    cover: str = None
    banner: str = None
    name: str
    url: str
    description: str
    items_count: int
    owners_count: int
    collections_count: int
    floor_price_count: float
    volume_troded_count: float
    profit: float
    created_at: datetime

    page: PageInAccount

    updated_at: datetime

    class Meta:
        index = "account"


class AccountDetail(Account):
    pass


class AccountList(Account):
    # TODO: решить что выводить
    pass


class AccountListPage(BaseListPage):
    results: List[AccountList]


class AccountSimpleList(BaseSchema):
    id: str
    name: str
    logo: str = None


class AccountSimpleListPage(BaseListPage):
    results: List[AccountSimpleList]
