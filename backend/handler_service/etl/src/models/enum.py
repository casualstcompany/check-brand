from enum import Enum


class StatusTypeEnum(str, Enum):
    book = "book"
    mint_1 = "mint_1"
    mint_2 = "mint_2"
    stop = "stop"
    sold_out = "sold_out"


class TokenTypeEnum(str, Enum):
    standard = "standard"


class StatusPriceTypeEnum(str, Enum):
    auction = "auction"
    no_price = "no_price"
    price = "price"


class LevelsStatsTypeEnum(str, Enum):
    levels = "levels"
    stats = "stats"
