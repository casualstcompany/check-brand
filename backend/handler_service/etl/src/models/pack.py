from datetime import datetime
from typing import Optional, List

from pydantic import validator

from models.base import BaseExtractLoadSchema, BaseComponentExtractLoadSchema
from models.enum import TokenTypeEnum, StatusPriceTypeEnum, StatusTypeEnum, LevelsStatsTypeEnum


class CreatorRoyaltyDistributionsInPack(BaseComponentExtractLoadSchema):
    id: str
    percent: str
    wallet: str

    class Meta:
        schema = "content"
        table = "creator_royalty_distribution"
        array_agg = "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object(" \
                    "'id', creator_royalty_distributions_pack.id, " \
                    "'percent', creator_royalty_distributions_pack.percent, " \
                    "'wallet', creator_royalty_distributions_pack.wallet " \
                    ")))) AS creator_royalty_distributions"
        left_join = "LEFT JOIN content.pack_creator_royalty_distribution " \
                    "AS relationship_creator_royalty_distributions_pack " \
                    "ON pack.id = relationship_creator_royalty_distributions_pack.pack_id " \
                    "LEFT JOIN content.creator_royalty_distribution AS creator_royalty_distributions_pack " \
                    "ON relationship_creator_royalty_distributions_pack.creatorroyaltydistribution_id " \
                    "= creator_royalty_distributions_pack.id"


class IncomeDistributionsInPack(BaseComponentExtractLoadSchema):
    id: str
    percent: str
    wallet: str

    class Meta:
        schema = "content"
        table = "income_distribution"
        array_agg = "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object(" \
                    "'id', income_distributions_pack.id, " \
                    "'percent', income_distributions_pack.percent, " \
                    "'wallet', income_distributions_pack.wallet " \
                    ")))) AS income_distributions"
        left_join = "LEFT JOIN content.pack_income_distribution AS relationship_income_distributions_pack " \
                    "ON pack.id = relationship_income_distributions_pack.pack_id " \
                    "LEFT JOIN content.income_distribution AS income_distributions_pack " \
                    "ON relationship_income_distributions_pack.incomedistribution_id = income_distributions_pack.id"


class PropertiesInPack(BaseComponentExtractLoadSchema):
    id: str
    name: str
    type: str

    class Meta:
        schema = "content"
        table = "properties"
        array_agg = "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object(" \
                    "'id', properties_pack.id, " \
                    "'name', properties_pack.name, " \
                    "'type', properties_pack.type " \
                    ")))) AS properties"
        left_join = "LEFT JOIN content.pack_properties AS relationship_properties_pack " \
                    "ON pack.id = relationship_properties_pack.pack_id " \
                    "LEFT JOIN content.properties AS properties_pack " \
                    "ON relationship_properties_pack.properties_id = properties_pack.id"


class LevelsStatsInPack(BaseComponentExtractLoadSchema):
    id: str
    name: str
    type: LevelsStatsTypeEnum
    value_1: int
    value_2: int

    class Meta:
        schema = "content"
        table = "levels_stats"
        array_agg = "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object(" \
                    "'id', levels_stats_pack.id, " \
                    "'name', levels_stats_pack.name, " \
                    "'type', levels_stats_pack.type, " \
                    "'value_1', levels_stats_pack.value_1, " \
                    "'value_2', levels_stats_pack.value_2 " \
                    ")))) AS levels_stats"
        left_join = "LEFT JOIN content.pack_levels_stats AS relationship_levels_stats_pack " \
                    "ON pack.id = relationship_levels_stats_pack.pack_id " \
                    "LEFT JOIN content.levels_stats AS levels_stats_pack " \
                    "ON relationship_levels_stats_pack.levelsstats_id = levels_stats_pack.id"


class CollectionInPack(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "collection"
        array_agg = "(ARRAY_AGG(jsonb_build_object('id', collection_pack.id, " \
                    "'name', collection_pack.name)))[1] AS collection"
        left_join = " LEFT JOIN content.collection AS collection_pack ON pack.collection_id = collection_pack.id"


class CurrencyTokenInPack(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "currency_token"
        array_agg = "(ARRAY_AGG(" \
                    "jsonb_build_object('id', currency_token_pack.id, 'name', currency_token_pack.name)" \
                    "))[1] AS currency_token"
        left_join = " LEFT JOIN content.currency_token AS currency_token_pack " \
                    "ON pack.currency_token_id = currency_token_pack.id"


class PackExtractLoad(BaseExtractLoadSchema):
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
        schema = "content"
        table = "pack"
        file_mapping = "load/schemas/es_pack.json"
        field_group_by = "id"
        state_key_update_at = "pack_updated_at"

    @validator('levels_stats', 'properties', 'income_distributions', 'creator_royalty_distributions', pre=True)
    def validate_m2m(cls, v):
        """
            Так как это не обязательные поля с БД может вернуться что то вроде [{}],
            а схема это воспримет как объект и будет проверять поля, на что вылезут не нужные ошибки.
        """
        if v == [{}]:
            return None
        return v
