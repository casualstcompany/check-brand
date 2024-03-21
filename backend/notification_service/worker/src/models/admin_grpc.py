import uuid

from models.base import ApiBaseModel


class TemplateMail(ApiBaseModel):
    id: uuid.UUID
    subject: str
    body_html: str
    body_text: str
    content_type: str
