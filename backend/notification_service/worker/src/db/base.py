from abc import ABC, abstractmethod
from typing import Any


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


class MessageBrokerDB(ConnectionHandler, AsyncFactory, ABC):

    unicast_queue: str
    multicast_queue: str

    def __init__(self, connection: Any, queue_broker: Any) -> None:
        super().__init__(connection)
        self.connection = connection
        self.queue_broker = queue_broker
