import uuid
from typing import Any

from models.base import ApiBaseModel


class QueueMessage(ApiBaseModel):
    notification_id: uuid.UUID
    content_type: str
    payload: dict[str, Any]
