from datetime import datetime
from typing import Optional, List

from models.base import BaseSchema, BaseListPage
from models.collection import CollectionInToken
from models.enum import TokenTypeEnum, StatusPriceTypeEnum, StatusTypeEnum
from models.extra import (
    CurrencyTokenInToken,
    CreatorRoyaltyDistributionsInToken,
    IncomeDistributionsInToken,
    PropertiesInToken,
    LevelsStatsInToken,
)
from models.pack import PackInToken


class Token(BaseSchema):
    id: str
    wallet_owner: Optional[str] = None
    hide: Optional[bool] = None
    block: bool
    number: Optional[int] = None
    mint: Optional[bool] = None
    paid: Optional[bool] = None
    email: Optional[str] = None
    upload_blockchain: Optional[bool] = None
    freeze: Optional[bool] = None
    profit: Optional[str] = None
    type: Optional[TokenTypeEnum] = None
    name: str
    price: int
    status_price: Optional[StatusPriceTypeEnum] = None
    investor_royalty: str
    creator_royalty: str
    description: str
    close: Optional[bool] = None
    close_image: Optional[str] = None
    unlockable: Optional[bool] = None
    unlockable_content: Optional[str] = None
    status: Optional[StatusTypeEnum] = None
    address: Optional[str] = None
    file_1: Optional[str] = None
    file_2: Optional[str] = None
    file_1_name_ext: Optional[str] = None
    file_2_name_ext: Optional[str] = None
    url_opensea: Optional[str] = None
    currency_token: CurrencyTokenInToken
    creator_royalty_distributions: Optional[
        List[CreatorRoyaltyDistributionsInToken]
    ] = None
    income_distributions: Optional[List[IncomeDistributionsInToken]] = None
    properties: Optional[List[PropertiesInToken]] = None
    levels_stats: Optional[List[LevelsStatsInToken]] = None
    collection: CollectionInToken
    pack: PackInToken
    updated_at: datetime = None
    created_at: datetime = None

    class Meta:
        index = "token"
        to_usd = {}


class TokenDetail(Token):
    price_in_usd: Optional[str] = None


class TokenList(Token):
    # TODO: решить что выводить
    pass


class TokenListPage(BaseListPage):
    results: List[TokenList]
