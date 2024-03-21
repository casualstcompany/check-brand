import logging
import uuid

import grpc
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict
from typing_extensions import Any

from grpc_components.base_grpc_client import GrpcClient
from core.config import get_settings as settings
from grpc_components.protobufs.notification_api_pb2 import NotificationRequest
from grpc_components.protobufs.notification_api_pb2_grpc import NotificationStub


class NotificationGrpcClient(GrpcClient):
    stub = NotificationStub

    @classmethod
    async def create(cls) -> Any:
        # TODO: сделать через сертификат
        channel = grpc.aio.insecure_channel(f"{settings.NOTIFICATION_GRPC.HOST}:{settings.NOTIFICATION_GRPC.PORT}")
        return cls(channel)

    @classmethod
    def create_sync(cls) -> Any:
        # TODO: сделать через сертификат
        channel = grpc.insecure_channel(f"{settings.NOTIFICATION_GRPC.HOST}:{settings.NOTIFICATION_GRPC.PORT}")
        return cls(channel)

    async def notify_email_unicast_default(self, payload_dict: dict, content_type: str):
        """Все настройки отправки производим в этом методе"""
        payload = Struct()
        payload.update(payload_dict)
        body_request = {
            "id": str(uuid.uuid4()),
            "content_type": content_type,
            "importance_type": 1,
            "transmission_type": 0,
            "carrier_type": 0
        }
        await self.notification_user(body_request=body_request, payload=payload)

    def notify_email_unicast_default_sync(self, payload_dict: dict, content_type: str):
        """Все настройки отправки производим в этом методе"""
        payload = Struct()
        payload.update(payload_dict)
        body_request = {
            "id": str(uuid.uuid4()),
            "content_type": content_type,
            "importance_type": 1,
            "transmission_type": 0,
            "carrier_type": 0
        }
        self.notification_user_sync(body_request=body_request, payload=payload)

    async def notification_user(self, body_request: dict, payload: Struct):
        """Конечная точка перед заказом на уведомление пользователя"""

        request = NotificationRequest(**body_request, payload=payload)
        response_data = {}
        try:
            response = await self.get_response_retrieve(retrieve=self.client.NotifyUser, request=request)
            response_data = MessageToDict(response, preserving_proto_field_name=True)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
        logging.info(f"grpc.RpcError -%s" % response_data)
        if response_data.get("status") == "success":
            return True

        return False

    def notification_user_sync(self, body_request: dict, payload: Struct):
        """Конечная точка перед заказом на уведомление пользователя"""

        request = NotificationRequest(**body_request, payload=payload)
        response_data = {}
        try:
            response = self.get_response_retrieve_sync(retrieve=self.client.NotifyUser, request=request)
            response_data = MessageToDict(response, preserving_proto_field_name=True)
        except grpc.RpcError as e:
            logging.error(f"grpc.RpcError - {e.code()}")
        logging.info(f"grpc.RpcError -%s" % response_data)
        if response_data.get("status") == "success":
            return True

        return False


client: NotificationGrpcClient
