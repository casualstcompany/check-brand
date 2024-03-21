import logging

import grpc
from google.protobuf.json_format import MessageToDict
from pydantic import ValidationError
from typing_extensions import Any

from grpc_components.base_grpc_client import GrpcClient
from core.config import get_settings as settings
from grpc_components.protobufs.nft_tokens_pb2 import CollectionRetrieveRequest, TokenRetrieveRequest
from grpc_components.protobufs.nft_tokens_pb2_grpc import CollectionGrpcControllerStub, TokenGrpcControllerStub

from schemas.admin_grpc import AdminCollectionSchema, AdminTokenSchema


class AdminGrpcClient(GrpcClient):
    stub = None

    def __init__(self, channel: Any) -> None:
        super().__init__(channel)
        self.channel = channel

    @classmethod
    async def create(cls) -> Any:
        # TODO: сделать через сертификат
        channel = grpc.aio.insecure_channel(f"{settings.ADMIN_GRPC.HOST}:{settings.ADMIN_GRPC.PORT}")
        return cls(channel)

    @classmethod
    def create_sync(cls) -> Any:
        # TODO: сделать через сертификат
        channel = grpc.insecure_channel(f"{settings.ADMIN_GRPC.HOST}:{settings.ADMIN_GRPC.PORT}")
        return cls(channel)

    async def get_collection(self, collection_id: str):

        request = CollectionRetrieveRequest(id=collection_id)
        new_client = CollectionGrpcControllerStub(self.channel)
        try:
            response = await self.get_response_retrieve_without_delay(retrieve=new_client.Retrieve, request=request)
            response_data = MessageToDict(response, preserving_proto_field_name=True)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
            return None, True

        try:
            return AdminCollectionSchema(**response_data), None
        except ValidationError:
            logging.error("AdminCollectionSchema - ValidationError")
            return None, True

    def get_collection_sync(self, collection_id: str):

        request = CollectionRetrieveRequest(id=collection_id)
        new_client = CollectionGrpcControllerStub(self.channel)
        try:
            response = self.get_response_retrieve_sync(retrieve=new_client.Retrieve, request=request)
            response_data = MessageToDict(response, preserving_proto_field_name=True)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
            return None, True

        try:
            return AdminCollectionSchema(**response_data), None
        except ValidationError:
            logging.error("AdminCollectionSchema - ValidationError")
            return None, True

    async def get_token(self, token_id: str):

        request = TokenRetrieveRequest(id=token_id)
        new_client = TokenGrpcControllerStub(self.channel)
        try:
            response = await self.get_response_retrieve(retrieve=new_client.Retrieve, request=request)
            response_data = MessageToDict(response, preserving_proto_field_name=True)
            logging.info(response_data)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
            return None, True

        try:
            return AdminTokenSchema(**response_data), None
        except ValidationError:
            logging.error("AdminTokenSchema - ValidationError")
            return None, True


client: AdminGrpcClient
