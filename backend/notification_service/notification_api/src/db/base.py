from abc import ABC, abstractmethod
from typing import Any

from models.messages import QueueMessage


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


class MessageBrokerDB(ConnectionHandler, AsyncFactory):

    unicast_queue: str
    multicast_queue: str

    def __init__(self, connection: Any, topic_declare_exchange: Any) -> None:
        super().__init__(connection)
        self.connection = connection
        self.topic_declare_exchange = topic_declare_exchange

    @abstractmethod
    async def put(self, message: QueueMessage, carrier_type: str, transmission_type: str, importance_type: str) -> None:
        pass


class CacheBase(ConnectionHandler, AsyncFactory):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int) -> None:
        pass
