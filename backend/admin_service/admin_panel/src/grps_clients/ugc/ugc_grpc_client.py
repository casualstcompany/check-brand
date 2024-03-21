# import logging
#
# import backoff
# import grpc
# from google.protobuf.json_format import MessageToDict
#
# from grps_clients.ugc.protobufs.ugc_grpc_pb2_grpc import UgcGRPCStub
# from grps_clients.ugc.protobufs.ugc_grpc_pb2 import (
# UpdateApplicationByStatusRequest, ListApplicationWhiteListRequest)
# from grps_clients.ugc.settings import ugc_grpc_settings
#
#
# channel = grpc.insecure_channel(f"{ugc_grpc_settings.HOST_GRPC}:{ugc_grpc_settings.PORT_GRPC}")
# client = UgcGRPCStub(channel)
#
#
# @backoff.on_exception(backoff.expo, grpc.RpcError, max_tries=7, jitter=None)
# def update_applications_by_collection_id(status_token: str, collection_id: str):
#     logging.debug("start")
#     logging.debug(f"{ugc_grpc_settings.HOST_GRPC}:{ugc_grpc_settings.PORT_GRPC}")
#
#     ugc_grpc_requests = UpdateApplicationByStatusRequest(
#         status_token=status_token,
#         collection_id=collection_id
#     )
#     ugc_grpc_response = None
#
#     try:
#         ugc_grpc_response = client.UpdateApplicationByStatus(ugc_grpc_requests, )
#         ugc_grpc_response = MessageToDict(ugc_grpc_response, preserving_proto_field_name=True)
#
#     except grpc.RpcError as e:
#         logging.error("grpc.RpcError")
#         logging.error(e)
#
#     logging.debug("finish")
#     return ugc_grpc_response
#
#
# @backoff.on_exception(backoff.expo, grpc.RpcError, max_tries=7, jitter=None)
# def get_email_users_from_application_with_white_list(collection_id: str):
#     logging.debug("start")
#     logging.debug(f"{ugc_grpc_settings.HOST_GRPC}:{ugc_grpc_settings.PORT_GRPC}")
#
#     ugc_grpc_requests = ListApplicationWhiteListRequest(
#         collection_id=collection_id
#     )
#     ugc_grpc_response = None
#
#     try:
#         ugc_grpc_response = client.ListApplicationWhiteList(ugc_grpc_requests, )
#         ugc_grpc_response = MessageToDict(ugc_grpc_response, preserving_proto_field_name=True)
#
#     except grpc.RpcError as e:
#         logging.error("grpc.RpcError")
#         logging.error(e)
#
#     logging.debug("finish")
#     return ugc_grpc_response
