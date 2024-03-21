import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType

from models.base import BaseModel, DateTimeMixin, UUIDMixin


class StatusApplicationEnum(str, enum.Enum):
    white = "white"
    read = "read"
    new = "new"


class Application(BaseModel, UUIDMixin, DateTimeMixin):
    __tablename__ = "application"
    __table_args__ = ({"schema": "content"})

    status = Column(Enum(StatusApplicationEnum),  default=StatusApplicationEnum.new.value)
    collection_id = Column(UUID(as_uuid=True))
    token_id = Column(UUID(as_uuid=True), nullable=True)

    user_wallet = Column(String)
    moderator_wallet = Column(String, nullable=True)

    number = Column(Integer, default=0)
    in_work = Column(Boolean, default=False)
    hide = Column(Boolean, default=False)

    field_1 = Column(String, nullable=True)
    field_2 = Column(String, nullable=True)
    field_3 = Column(String, nullable=True)
    field_4 = Column(String, nullable=True)
    field_5 = Column(String, nullable=True)
    field_6 = Column(String, nullable=True)
    field_7 = Column(String, nullable=True)
    field_8 = Column(String, nullable=True)
    field_9 = Column(String, nullable=True)
    field_10 = Column(String, nullable=True)
    description = Column(Text)

    email = Column(EmailType)
    discord_name = Column(String)
