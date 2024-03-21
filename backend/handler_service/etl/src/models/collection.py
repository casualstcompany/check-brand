from datetime import datetime
from typing import Optional, List

from pydantic import validator

from models.base import BaseExtractLoadSchema, BaseComponentExtractLoadSchema
from models.enum import TokenTypeEnum, StatusTypeEnum


class CurrencyTokenInCollection(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "currency_token"
        array_agg = "(ARRAY_AGG(DISTINCT jsonb_strip_nulls(jsonb_build_object(" \
                    "'id', payment_tokens_collection.id, " \
                    "'name', payment_tokens_collection.name " \
                    ")))) AS payment_tokens"
        left_join = "LEFT JOIN content.collection_payment_tokens AS relationship_payment_tokens_collection " \
                    "ON collection.id = relationship_payment_tokens_collection.collection_id " \
                    "LEFT JOIN content.currency_token AS payment_tokens_collection " \
                    "ON relationship_payment_tokens_collection.currencytoken_id = payment_tokens_collection.id"


class AccountInCollection(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "account"
        array_agg = "(ARRAY_AGG(jsonb_build_object('id', account_collection.id, " \
                    "'name', account_collection.name)))[1] AS account"
        left_join = " LEFT JOIN content.account AS account_collection ON collection.account_id = account_collection.id"


class BlockchainInCollection(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "blockchain"
        array_agg = "(ARRAY_AGG(jsonb_build_object('id', blockchain_collection.id, " \
                    "'name', blockchain_collection.name)))[1] AS blockchain"
        left_join = " LEFT JOIN content.blockchain AS blockchain_collection " \
                    "ON collection.blockchain_id = blockchain_collection.id"


class PageInCollection(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "page"
        array_agg = "(ARRAY_AGG(jsonb_build_object('id', page_collection.id, " \
                    "'name', page_collection.name)))[1] AS page"
        left_join = " LEFT JOIN content.page AS page_collection " \
                    "ON collection.page_id = page_collection.id"


class CollectionExtractLoad(BaseExtractLoadSchema):
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
    application_form: str
    symbol: str
    percentage_fee: float
    display_theme: str
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
        schema = "content"
        table = "collection"
        file_mapping = "load/schemas/es_collection.json"
        field_group_by = "id"
        state_key_update_at = "collection_updated_at"

    @validator('payment_tokens', pre=True)
    def validate_m2m(cls, v):
        """
            Так как это не обязательные поля с БД может вернуться что то вроде [{}],
            а схема это воспримет как объект и будет проверять поля, на что вылезут не нужные ошибки.
        """
        if v == [{}]:
            return None
        return v
