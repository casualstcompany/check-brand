from datetime import datetime
from typing import Optional, List

from pydantic import validator

from models.base import BaseExtractLoadSchema, BaseComponentExtractLoadSchema
from models.enum import (
    TokenTypeEnum,
    StatusPriceTypeEnum,
    StatusTypeEnum,
    LevelsStatsTypeEnum,
)


class CreatorRoyaltyDistributionsInToken(BaseComponentExtractLoadSchema):
    id: str
    percent: str
    wallet: str

    class Meta:
        schema = "content"
        table = "creator_royalty_distribution"
        array_agg = (
            "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object("
            "'id', creator_royalty_distributions_token.id, "
            "'percent', creator_royalty_distributions_token.percent, "
            "'wallet', creator_royalty_distributions_token.wallet "
            ")))) AS creator_royalty_distributions"
        )
        left_join = (
            "LEFT JOIN content.token_creator_royalty_distribution AS"
            " relationship_creator_royalty_distributions_token ON token.id ="
            " relationship_creator_royalty_distributions_token.token_id LEFT"
            " JOIN content.creator_royalty_distribution AS"
            " creator_royalty_distributions_token ON"
            " relationship_creator_royalty_distributions_token.creatorroyaltydistribution_id"
            " = creator_royalty_distributions_token.id"
        )


class IncomeDistributionsInToken(BaseComponentExtractLoadSchema):
    id: str
    percent: str
    wallet: str

    class Meta:
        schema = "content"
        table = "income_distribution"
        array_agg = (
            "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object("
            "'id', income_distributions_token.id, "
            "'percent', income_distributions_token.percent, "
            "'wallet', income_distributions_token.wallet "
            ")))) AS income_distributions"
        )
        left_join = (
            "LEFT JOIN content.token_income_distribution AS"
            " relationship_income_distributions_token ON token.id ="
            " relationship_income_distributions_token.token_id LEFT JOIN"
            " content.income_distribution AS income_distributions_token ON"
            " relationship_income_distributions_token.incomedistribution_id ="
            " income_distributions_token.id"
        )


class PropertiesInToken(BaseComponentExtractLoadSchema):
    id: str
    name: str
    type: str

    class Meta:
        schema = "content"
        table = "properties"
        array_agg = (
            "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object("
            "'id', properties_token.id, "
            "'name', properties_token.name, "
            "'type', properties_token.type "
            ")))) AS properties"
        )
        left_join = (
            "LEFT JOIN content.token_properties AS"
            " relationship_properties_token ON token.id ="
            " relationship_properties_token.token_id LEFT JOIN"
            " content.properties AS properties_token ON"
            " relationship_properties_token.properties_id ="
            " properties_token.id"
        )


class LevelsStatsInToken(BaseComponentExtractLoadSchema):
    id: str
    name: str
    type: LevelsStatsTypeEnum
    value_1: int
    value_2: int

    class Meta:
        schema = "content"
        table = "levels_stats"
        array_agg = (
            "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object("
            "'id', levels_stats_token.id, "
            "'name', levels_stats_token.name, "
            "'type', levels_stats_token.type, "
            "'value_1', levels_stats_token.value_1, "
            "'value_2', levels_stats_token.value_2 "
            ")))) AS levels_stats"
        )
        left_join = (
            "LEFT JOIN content.token_levels_stats AS"
            " relationship_levels_stats_token ON token.id ="
            " relationship_levels_stats_token.token_id LEFT JOIN"
            " content.levels_stats AS levels_stats_token ON"
            " relationship_levels_stats_token.levelsstats_id ="
            " levels_stats_token.id"
        )


class CollectionInToken(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "collection"
        array_agg = (
            "(ARRAY_AGG(jsonb_build_object('id', collection_token.id, "
            "'name', collection_token.name)))[1] AS collection"
        )
        left_join = (
            " LEFT JOIN content.collection AS collection_token ON"
            " token.collection_id = collection_token.id"
        )


class CurrencyTokenInToken(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "currency_token"
        array_agg = (
            "(ARRAY_AGG(jsonb_build_object('id', currency_token_token.id,"
            " 'name', currency_token_token.name)))[1] AS currency_token"
        )
        left_join = (
            " LEFT JOIN content.currency_token AS currency_token_token "
            "ON token.currency_token_id = currency_token_token.id"
        )


class PackInToken(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "pack"
        array_agg = (
            "(ARRAY_AGG(jsonb_build_object('id', pack_token.id, 'name',"
            " pack_token.name)))[1] AS pack"
        )
        left_join = (
            " LEFT JOIN content.pack AS pack_token ON token.pack_id ="
            " pack_token.id"
        )


class TokenExtractLoad(BaseExtractLoadSchema):
    wallet_owner: Optional[str] = None
    hide: bool
    block: bool
    number: Optional[int] = None
    mint: bool
    paid: bool
    email: Optional[str] = None
    upload_blockchain: bool
    freeze: bool
    profit: float
    type: TokenTypeEnum
    name: str
    price: int
    status_price: StatusPriceTypeEnum
    investor_royalty: float
    creator_royalty: float
    description: str
    close: bool
    close_image: Optional[str] = None
    unlockable: bool
    unlockable_content: Optional[str] = None
    status: StatusTypeEnum
    address: Optional[str] = None
    file_1: Optional[str] = None
    file_2: Optional[str] = None
    file_1_name_ext: Optional[str] = None
    file_2_name_ext: Optional[str] = None
    url_opensea: Optional[str] = None
    created_at: datetime = None
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

    class Meta:
        schema = "content"
        table = "token"
        file_mapping = "load/schemas/es_token.json"
        field_group_by = "id"
        state_key_update_at = "token_updated_at"

    @validator(
        "levels_stats",
        "properties",
        "income_distributions",
        "creator_royalty_distributions",
        pre=True,
    )
    def validate_m2m(cls, v):
        """
        Так как это не обязательные поля с БД может вернуться что то вроде [{}],
        а схема это воспримет как объект и будет проверять поля, на что вылезут не нужные ошибки.
        """
        if v == [{}]:
            return None
        return v
