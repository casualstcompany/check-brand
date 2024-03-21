from uuid import uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class DateTimeMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


BaseModel = declarative_base()
