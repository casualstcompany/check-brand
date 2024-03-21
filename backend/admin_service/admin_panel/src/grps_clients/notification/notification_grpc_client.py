# import logging
# import uuid
#
# import backoff
# import grpc
# from google.protobuf.json_format import MessageToDict
# from google.protobuf.struct_pb2 import Struct
#
# from grps_clients.notification.protobufs.notification_api_pb2_grpc import NotificationStub
# from grps_clients.notification.protobufs.notification_api_pb2 import NotificationRequest
# from grps_clients.notification.settings import notification_grpc_settings
#
#
# channel = grpc.insecure_channel(
# f"{notification_grpc_settings.HOST_GRPC}:{notification_grpc_settings.PORT_GRPC}")
# client = NotificationStub(channel)
#
#
# def notify_email_multicast_default(payload_dict: dict, content_type: str):
#     """ Все настройки отправки производим в этом методе."""
#
#     logging.debug("Преобразование данных")
#
#     payload = Struct()
#     payload.update(payload_dict)
#     body_request = {
#         "id": str(uuid.uuid4()),
#         "content_type": content_type,
#         "importance_type": 1,
#         "transmission_type": 1,
#         "carrier_type": 0
#     }
#     logging.debug(payload)
#     logging.debug(body_request)
#     return notification_user(body_request=body_request, payload=payload)
#
#
# @backoff.on_exception(backoff.expo, grpc.RpcError, max_tries=7, jitter=None)
# def notification_user(body_request: dict, payload: Struct):
#     """Конечная точка перед заказом на уведомление пользователя"""
#
#     logging.debug(
#     f"{notification_grpc_settings.HOST_GRPC}:{notification_grpc_settings.PORT_GRPC}")
#
#     request = NotificationRequest(**body_request, payload=payload)
#     response_data = {}
#
#     try:
#         response = client.NotifyUser(request)
#         response_data = MessageToDict(response, preserving_proto_field_name=True)
#     except grpc.RpcError as e:
#         logging.error("grpc.RpcError")
#         logging.error(e)
#         raise e
#
#     if response_data.get("status") == "success":
#         logging.debug("notification send")
#         return True
#
#     logging.debug("notification not send")
#     return False
