import abc
from abc import ABC, abstractmethod
from typing import Any


class BaseDBManager(ABC):

    @abc.abstractmethod
    def get_by_id(self, index: str, obj_id: str):
        pass

    @abc.abstractmethod
    def search_data(self, index, body=None):
        pass


class AsyncFactory(ABC):

    @classmethod
    @abstractmethod
    async def create(cls) -> Any:
        pass


class ConnectionHandler:

    def __init__(self, connection: Any) -> None:
        self.connection = connection

    async def close(self) -> None:
        await self.connection.close()


class CacheBase(ConnectionHandler, AsyncFactory):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int):
        pass
