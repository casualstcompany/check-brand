from datetime import datetime
from typing import Optional, List

from models.account import AccountInCollection
from models.base import BaseSchema, BaseListPage
from models.enum import TokenTypeEnum, StatusTypeEnum
from models.extra import CurrencyTokenInCollection, BlockchainInCollection
from models.page import PageInCollection


class BaseCollectionIn(BaseSchema):
    id: str
    name: str


class CollectionInToken(BaseCollectionIn):
    pass


class CollectionInPack(BaseCollectionIn):
    pass


class Collection(BaseSchema):
    id: str
    hide: bool
    link_opensea: str = None
    link_discord: str = None
    link_instagram: str = None
    link_medium: str = None
    link_twitter: str = None
    type: TokenTypeEnum
    logo: str = None
    featured: str = None
    banner: str = None
    name: str
    url: str
    url_opensea: str = None
    percentage_fee: float
    display_theme: str
    application_form: str
    symbol: str
    description: str
    upload_blockchain: bool
    smart_contract_address: str = None
    items_count: int
    owners_count: int
    floor_price_count: float
    volume_troded_count: float
    profit: float
    creator_profit: float
    creator_fee: float
    status: StatusTypeEnum

    created_at: datetime

    account: AccountInCollection
    blockchain: BlockchainInCollection
    page: PageInCollection

    payment_tokens: Optional[List[CurrencyTokenInCollection]] = None

    updated_at: datetime = None

    class Meta:
        index = "collection"


class CollectionDetail(Collection):
    pass


class CollectionList(Collection):
    # TODO: решить что выводить
    pass


class CollectionListRankings(BaseSchema):
    id: str
    logo: str = None
    name: str
    url: str
    items_count: int
    owners_count: int
    floor_price_count: float
    volume_troded_count: float
    status: StatusTypeEnum

    blockchain: BlockchainInCollection
    page: PageInCollection

    payment_tokens: Optional[List[CurrencyTokenInCollection]] = None
    created_at: datetime
    updated_at: datetime = None


class CollectionSimpleList(BaseSchema):
    id: str
    name: str
    logo: str = None
    account_id: str


class CollectionListPage(BaseListPage):
    results: List[CollectionList]


class CollectionListRankingsPage(BaseListPage):
    results: List[CollectionListRankings]


class CollectionSimpleListPage(BaseListPage):
    results: List[CollectionSimpleList]
