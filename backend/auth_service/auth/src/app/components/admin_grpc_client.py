import logging
from typing import Any

import grpc
from components.base_grpc_client import GrpcClient
from components.protobufs.nft_tokens_pb2 import CollectionRetrieveRequest
from components.protobufs.nft_tokens_pb2_grpc import (
    CollectionGrpcControllerStub,
)
from config.config import config as settings
from google.protobuf.json_format import MessageToDict
from pydantic import ValidationError
from schemes.admin_grpc import AdminCollectionSchema


class AdminGrpcClient(GrpcClient):
    stub = None

    def __init__(self, channel: Any) -> None:
        super().__init__(channel)
        self.channel = channel

    @classmethod
    def create(cls) -> Any:
        # TODO: сделать через сертификат
        channel = grpc.insecure_channel(
            f"{settings.ADMIN_GRPC.HOST}:{settings.ADMIN_GRPC.PORT}"
        )
        return cls(channel)

    def get_collection(self, collection_id: str):
        request = CollectionRetrieveRequest(id=collection_id)
        new_client = CollectionGrpcControllerStub(self.channel)

        try:
            response = self.get_response_retrieve(
                retrieve=new_client.Retrieve, request=request
            )
            response_data = MessageToDict(
                response, preserving_proto_field_name=True
            )
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
            return None, True

        try:
            return AdminCollectionSchema(**response_data), None
        except ValidationError as e:
            logging.error("AdminCollectionSchema - ValidationError")
            return None, True


client: AdminGrpcClient
