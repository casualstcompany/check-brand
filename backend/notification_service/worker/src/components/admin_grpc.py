import logging
from typing import Any

import grpc
from google.protobuf.json_format import MessageToDict

from components.base_grpc_client import GrpcClient
from components.protobufs.notification_pb2 import TemplateMailRetrieveRequest
from components.protobufs.notification_pb2_grpc import \
    TemplateMailControllerStub
from core.config import get_settings as settings
from core.utils import validation_model
from models.admin_grpc import TemplateMail


class AdminGrpcClient(GrpcClient):
    model = TemplateMail

    @classmethod
    async def create(cls) -> Any:
        channel = grpc.aio.insecure_channel(f"{settings.ADMIN_GRPC.HOST}:{settings.ADMIN_GRPC.PORT}")
        return cls(channel)

    async def get_template_mail(self, content_type: str):
        client = TemplateMailControllerStub(self.channel)
        request = TemplateMailRetrieveRequest(content_type=content_type)
        error = False

        try:
            response = await self.get_response_retrieve(client, request)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
            error = "ERROR"

            if e.code() == grpc.StatusCode.UNAVAILABLE:
                error = "UNAVAILABLE"

            return False, error
        response_data = MessageToDict(response, preserving_proto_field_name=True)

        valid_model = validation_model(self.model, response_data)

        if not valid_model:
            error = "INVALID_MODEL"
            return False, error

        return valid_model, error


admin_grpc_client: AdminGrpcClient
