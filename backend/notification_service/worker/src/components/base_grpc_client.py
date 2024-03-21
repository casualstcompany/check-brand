import logging
from abc import ABC, abstractmethod
from typing import Any

import backoff
import grpc

from core.error import UnavailableException


class AsyncFactory(ABC):

    @classmethod
    @abstractmethod
    async def create(cls) -> Any:
        pass


class ChannelHandler:

    def __init__(self, channel: Any) -> None:
        self.channel = channel

    async def close(self) -> None:
        await self.channel.close()


class GrpcClient(ChannelHandler, AsyncFactory, ABC):

    @staticmethod
    @backoff.on_exception(backoff.expo, UnavailableException, max_tries=7, jitter=None)
    async def get_response_retrieve(client, request):
        logging.debug("get_response_retrieve")
        try:
            return await client.Retrieve(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise UnavailableException
            raise e
