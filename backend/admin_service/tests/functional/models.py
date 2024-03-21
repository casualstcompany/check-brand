from datetime import datetime
from uuid import uuid4

from functional.config import config
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, MetaData,
                        String, Text, UniqueConstraint, create_engine, Integer)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


db_config = config.DatabaseConfig()
metadata_obj = MetaData(schema=db_config.SCHEMA)
Base = declarative_base(db_config.ENGINE, metadata=metadata_obj)


class DateTimeMixin:
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


class Page(Base, DateTimeMixin):
    __tablename__ = "page"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    hide = Column(Boolean(), default=False)
    name = Column(String(255), unique=True, nullable=False)
    number = Column(Integer(), unique=True)
    url = Column(String(30), unique=True)
    banner = Column(String())
    title_1 = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    title_2 = Column(String(255), nullable=False)
