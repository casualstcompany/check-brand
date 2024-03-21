from models.base import BaseSchema
from models.enum import LevelsStatsTypeEnum


class BaseCreatorRoyaltyDistributionsIn(BaseSchema):
    id: str
    percent: str
    wallet: str


class CreatorRoyaltyDistributionsInToken(BaseCreatorRoyaltyDistributionsIn):
    pass


class CreatorRoyaltyDistributionsInPack(BaseCreatorRoyaltyDistributionsIn):
    pass


class BaseIncomeDistributionsIn(BaseSchema):
    id: str
    percent: str
    wallet: str


class IncomeDistributionsInToken(BaseIncomeDistributionsIn):
    pass


class IncomeDistributionsInPack(BaseIncomeDistributionsIn):
    pass


class BasePropertiesIn(BaseSchema):
    id: str
    name: str
    type: str


class PropertiesInToken(BasePropertiesIn):
    pass


class PropertiesInPack(BasePropertiesIn):
    pass


class BaseLevelsStatsIn(BaseSchema):
    id: str
    name: str
    type: LevelsStatsTypeEnum
    value_1: int
    value_2: int


class LevelsStatsInToken(BaseLevelsStatsIn):
    pass


class LevelsStatsInPack(BaseLevelsStatsIn):
    pass


class BaseCurrencyTokenIn(BaseSchema):
    id: str
    name: str


class CurrencyTokenInToken(BaseCurrencyTokenIn):
    pass


class CurrencyTokenInPack(BaseCurrencyTokenIn):
    pass


class CurrencyTokenInCollection(BaseCurrencyTokenIn):
    pass


class BlockchainIn(BaseSchema):
    id: str
    name: str


class BlockchainInCollection(BlockchainIn):
    pass
