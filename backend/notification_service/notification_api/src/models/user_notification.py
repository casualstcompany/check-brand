import uuid
from typing import Any

from .base import ApiBaseModel


class UserNotificationExternalModel(ApiBaseModel):
    id: uuid.UUID
    content_type: str
    importance_type: str
    transmission_type: str
    carrier_type: str
    payload: dict[str, Any]
