from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import get_settings as settings

SQLALCHEMY_DATABASE_URL = \
    f"{settings.POSTGRES.USERNAME}:{settings.POSTGRES.PASSWORD}" \
    f"@{settings.POSTGRES.HOST}:{settings.POSTGRES.PORT}" \
    f"/{settings.POSTGRES.DATABASE}"

"""Оставил для миграций"""
engine = create_engine(
    f"postgresql://{SQLALCHEMY_DATABASE_URL}"
)

asyncio_engine = create_async_engine(
    f"postgresql+asyncpg://{SQLALCHEMY_DATABASE_URL}",
    echo=True,
)

async_session = sessionmaker(asyncio_engine, expire_on_commit=False, class_=AsyncSession)
