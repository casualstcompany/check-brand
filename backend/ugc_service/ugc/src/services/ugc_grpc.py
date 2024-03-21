import logging

import grpc
from pydantic import ValidationError
from google.protobuf.json_format import MessageToDict

from grpc_components.protobufs import ugc_grpc_pb2, ugc_grpc_pb2_grpc
from schemas.application import UpdateApplicationByStatusRequestSchema, ListApplicationWhiteListRequestSchema, \
    ApplicationWhiteListResponseSchema
from services.application import application_service


class UgcGRPCService(ugc_grpc_pb2_grpc.UgcGRPCServicer):

    def __init__(self, app):
        self.app = app

    async def UpdateApplicationByStatus(self, request, context):
        """Метод обновляет данные в заявках
        при изменении статуса(этапа mint) в коллекциях
        """
        logging.debug("Start UpdateApplicationByStatus")
        schema = UpdateApplicationByStatusRequestSchema

        data = await self.get_data(request)

        validate_data = await self.validate_date(context, schema, data)
        if validate_data:

            await application_service.update_applications_by_status_tokens(
                status_token=validate_data.status_token,
                collection_id=validate_data.collection_id
            )
            logging.debug("Finish UpdateApplicationByStatus")
            return ugc_grpc_pb2.UpdateApplicationByStatusResponse(status="success")

        return ugc_grpc_pb2.UpdateApplicationByStatusResponse(status="error")

    async def ListApplicationWhiteList(self, request, context):
        """ Возвращает список заявок вайт листа по collection_id"""

        logging.debug("Start ListApplicationWhiteList")
        schema = ListApplicationWhiteListRequestSchema

        data = await self.get_data(request)
        validate_data = await self.validate_date(context, schema, data)
        response_data = []
        if validate_data:
            raw_response_data = await application_service.get_applications_by_params_for_grpc(params=validate_data)
            if raw_response_data:
                response_data = [
                    ApplicationWhiteListResponseSchema(
                        id=str(item.id),
                        user_wallet=item.user_wallet,
                        email=item.email,
                    ).dict() for item in raw_response_data]

        logging.debug("Finish ListApplicationWhiteList")
        return ugc_grpc_pb2.ListApplicationWhiteListResponse(data=response_data)

    @staticmethod
    async def get_data(request):
        """ Конвертирует из прото формата в json"""
        data = MessageToDict(
            request,
            preserving_proto_field_name=True,
            including_default_value_fields=True,
        )
        logging.debug("request %s " % request)
        return data

    async def validate_date(self, context, schema, request):
        try:
            return schema(**request)
        except ValidationError as e:
            logging.error(e.errors())
            await self.error(context, grpc.StatusCode.INVALID_ARGUMENT, "data is not valid")
            return None

    @staticmethod
    async def error(context, status, detail):
        context.set_code(status)
        context.set_details(detail)

# TODO написать несколько тестов на методы
