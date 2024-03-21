from datetime import datetime
from typing import Optional, List

from models.collection import CollectionInPack
from models.enum import TokenTypeEnum, StatusPriceTypeEnum, StatusTypeEnum
from models.base import BaseSchema, BaseListPage
from models.extra import CurrencyTokenInPack, CreatorRoyaltyDistributionsInPack, IncomeDistributionsInPack, \
    PropertiesInPack, LevelsStatsInPack


class PackInToken(BaseSchema):
    id: str
    name: str


class Pack(BaseSchema):
    id: str
    wallet_owner: Optional[str] = None
    hide: bool
    upload_blockchain: bool
    freeze: bool
    profit: float
    items_count: int
    type: TokenTypeEnum
    name: str
    price: float
    status_price: StatusPriceTypeEnum
    investor_royalty: float
    creator_royalty: float
    description: str
    close: bool
    block: bool
    close_image: Optional[str] = None
    unlockable: bool
    unlockable_content: Optional[str] = None
    status: StatusTypeEnum
    created_at: datetime = None

    currency_token: CurrencyTokenInPack
    creator_royalty_distributions: Optional[List[
        CreatorRoyaltyDistributionsInPack
    ]] = None
    income_distributions: Optional[List[IncomeDistributionsInPack]] = None
    properties: Optional[List[PropertiesInPack]] = None
    levels_stats: Optional[List[LevelsStatsInPack]] = None
    collection: CollectionInPack
    updated_at: datetime = None

    class Meta:
        index = "pack"


class PackDetail(Pack):
    pass


class PackList(Pack):
    # TODO: решить что выводить
    pass


class PackListPage(BaseListPage):
    results: List[PackList]
