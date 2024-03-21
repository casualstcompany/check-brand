from datetime import datetime

from models.base import BaseExtractLoadSchema, BaseComponentExtractLoadSchema


class PageExtractLoad(BaseExtractLoadSchema):
    hide: bool
    name: str
    number: int
    url: str
    banner: str = None
    title_1: str = None
    description: str = None
    title_2: str = None
    icon: str = None
    created_at: datetime
    updated_at: datetime

    class Meta:
        schema = "content"
        table = "page"
        file_mapping = "load/schemas/es_page.json"
        field_group_by = "id"
        state_key_update_at = "page_updated_at"
