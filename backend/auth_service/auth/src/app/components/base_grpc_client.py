import logging
from abc import ABC
from typing import Any

import backoff
import grpc
from components.base_error import UnavailableException


class ChannelHandler:
    stub: Any

    def __init__(self, channel: Any) -> None:
        self.channel = channel
        if self.stub:
            self.client = self.stub(channel)

    def close(self) -> None:
        self.channel.close()


class GrpcClient(ChannelHandler, ABC):
    @backoff.on_exception(
        backoff.expo, UnavailableException, max_tries=7, jitter=None
    )
    def get_response_retrieve(self, retrieve, request):
        logging.debug("get_response_retrieve")
        try:
            return retrieve(request)
        except grpc.RpcError as e:
            logging.info(e)
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise UnavailableException
            raise e
