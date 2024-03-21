from enum import Enum


class SortCreatedUpdatedEnum(str, Enum):
    desc_created_at = "-created_at"
    asc_created_at = "created_at"
    desc_updated_at = "-updated_at"
    asc_updated_at = "updated_at"
