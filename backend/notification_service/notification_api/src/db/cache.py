import aioredis
import backoff
from aioredis import Redis, RedisError

from core.config import get_settings as settings
from db.base import CacheBase


class CacheService(CacheBase):
    def __init__(self, connection: Redis):
        super().__init__(connection)
        self.connection = connection

    @classmethod
    async def create(cls) -> CacheBase:
        connection = aioredis.from_url(
            f"{settings.CACHE.DRIVER}://:{settings.CACHE.PASSWORD}@{settings.CACHE.HOST}:{settings.CACHE.PORT}/0",
            encoding="utf-8",
            decode_responses=True
        )
        return cls(connection=connection)

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def get(self, name: str):
        data = await self.connection.get(name)
        if not data:
            return False
        return True

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def set(self, name: str, value: int, expire: int) -> None:
        await self.connection.set(name=name, value=value, ex=expire)
