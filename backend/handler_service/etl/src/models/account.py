from datetime import datetime

from models.base import BaseExtractLoadSchema, BaseComponentExtractLoadSchema
from models.enum import TokenTypeEnum


class PageInAccount(BaseComponentExtractLoadSchema):
    id: str
    name: str

    class Meta:
        schema = "content"
        table = "page"
        array_agg = "(ARRAY_AGG(jsonb_build_object('id', page_account.id, " \
                    "'name', page_account.name)))[1] AS page"
        left_join = " LEFT JOIN content.page AS page_account " \
                    "ON account.page_id = page_account.id"


class AccountExtractLoad(BaseExtractLoadSchema):
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
        schema = "content"
        table = "account"
        file_mapping = "load/schemas/es_account.json"
        field_group_by = "id"
        state_key_update_at = "account_updated_at"
