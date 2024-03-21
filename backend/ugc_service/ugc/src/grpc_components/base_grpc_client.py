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

    stub: Any

    def __init__(self, channel: Any) -> None:
        self.channel = channel
        if self.stub:
            self.client = self.stub(channel)

    async def close(self) -> None:
        await self.channel.close()

    def close_sync(self) -> None:
        self.channel.close()


class GrpcClient(ChannelHandler, AsyncFactory, ABC):

    @backoff.on_exception(backoff.expo, UnavailableException, max_tries=7, jitter=None)
    async def get_response_retrieve(self, retrieve, request):
        logging.debug("get_response_retrieve")
        try:
            return await retrieve(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise UnavailableException
            raise e

    @backoff.on_exception(backoff.expo, UnavailableException, max_tries=7, jitter=None)
    def get_response_retrieve_sync(self, retrieve, request):
        logging.debug("get_response_retrieve_sync")
        try:
            return retrieve(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise UnavailableException
            raise e

    @staticmethod
    async def get_response_retrieve_without_delay(retrieve, request):
        logging.debug("get_response_retrieve_without_delay")
        try:
            return await retrieve(request)
        except grpc.RpcError as e:
            raise e
