import logging

import grpc
from components.grpc.protobufs.notification_api_pb2 import (
    NotificationRequest, NotificationResponse)
from google.protobuf.json_format import MessageToDict
from pydantic.error_wrappers import ValidationError

import db
from components.grpc.protobufs import notification_api_pb2_grpc
from models.messages import QueueMessage
from models.user_notification import UserNotificationExternalModel


class NotificationServicer(notification_api_pb2_grpc.NotificationServicer):

    async def NotifyUser(self, request, context):
        logging.debug('Receiving notifications from grpc other services')
        request = MessageToDict(
            request,
            preserving_proto_field_name=True,
            including_default_value_fields=True,
        )

        try:
            validation_data = UserNotificationExternalModel.parse_obj(request)
        except ValidationError as e:
            await self.error(context, grpc.StatusCode.INVALID_ARGUMENT, e.json())
            return NotificationResponse(status="error")

        duplicate = await db.cache.connection.get(name=str(validation_data.id))
        if duplicate:
            await self.error(context, grpc.StatusCode.ALREADY_EXISTS, "notification already exists")
            return NotificationResponse(status="error")

        try:
            await db.msg_broker.put(
                message=QueueMessage(
                    notification_id=validation_data.id,
                    content_type=validation_data.content_type,
                    payload=validation_data.payload
                ),
                carrier_type=validation_data.carrier_type,
                transmission_type=validation_data.transmission_type,
                importance_type=validation_data.importance_type
            )
            await db.cache.connection.set(name=str(validation_data.id), value=1)
        except Exception as e:
            logging.error(e)
            return NotificationResponse(status="error")

        return NotificationResponse(status="success")

    @staticmethod
    async def error(context, status, detail):
        context.set_code(status)
        context.set_details(detail)
