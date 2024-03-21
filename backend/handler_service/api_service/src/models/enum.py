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


class SortByTokenEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"
    desc_price = "-price"
    asc_price = "price"
    desc_number = "-number"
    asc_number = "number"


class SortByPackEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"
    desc_price = "-price"
    asc_price = "price"


class SortByCollectionEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"


class SortByCollectionRankingsEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"
    desc_volume_troded_count = "-volume_troded_count"
    asc_volume_troded_count = "volume_troded_count"
    desc_floor_price_count = "-floor_price_count"
    asc_floor_price_count = "floor_price_count"
    desc_items_count = "-items_count"
    asc_items_count = "items_count"
    desc_owners_count = "-owners_count"
    asc_owners_count = "owners_count"
    desc_status = "-status"
    asc_status = "status"


class SortByAccountEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"


class SortByPageEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"
