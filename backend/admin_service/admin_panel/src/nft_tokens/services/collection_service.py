import logging

from django import dispatch
from django.db.models import Count, Min, Q, Sum

# from grps_clients.notification.notification_grpc_client import (
#     notify_email_multicast_default,
# )
# from grps_clients.ugc import ugc_grpc_client
from nft_tokens.models import Collection
from nft_tokens.services.base_service import BaseService

# from nft_tokens.utils import get_content_type_by_status_collection

status_update_in_collection = dispatch.Signal()
logger = logging.getLogger(__name__)


class CollectionService(BaseService):
    model = Collection
    list_params = [
        "items_count",
        "owners_count",
        "floor_price_count",
        "volume_troded_count",
        "profit",
    ]

    def get_template_params_update(self):
        self.template_params_update = {
            "items_count": Count("token", distinct=True),
            "owners_count": Count(
                "token", distinct=True, filter=Q(token__mint=True)
            ),
            "floor_price_count": Min("token__price"),
            "volume_troded_count": Sum(
                "token__price", filter=Q(token__mint=True)
            ),
            "profit": Sum("token__price"),
        }

    def send_signal_status_update_in_collection(self, collection_id: str):
        status_update_in_collection.send(
            sender=self.__class__, collection_id=collection_id
        )

    @staticmethod
    def send_update_status_in_applications(status_token, collection_id):
        logger.info("send_update_status_in_application")
        status = True

        # update = ugc_grpc_client.update_applications_by_collection_id(
        #     status_token=status_token, collection_id=collection_id
        # )
        #
        # if not update:
        #     logger.info("re-queuing update_status_in_application")
        #     status = False

        return status

    @staticmethod
    def send_notification_users_with_white_list(
        status_token, collection_id, collection_name, collection_logo
    ):
        logger.info("Start send_notification_users_with_white_list")
        status = True

        # content_type = get_content_type_by_status_collection(status_token)
        # list_email_users = []
        # try:
        #     list_applications = ugc_grpc_client.get_email_users_from_application_with_white_list(
        #         collection_id=collection_id
        #     )
        #     if list_applications.get("data"):
        #         list_email_users = [
        #         application.get("email") for application in list_applications.get("data")
        #         ]
        # except Exception as e:
        #     raise e
        #
        # if content_type and list_email_users:
        #     payload = {
        #         "email": list_email_users,
        #         "collection_id": str(collection_id),
        #         "collection_name": collection_name,
        #         "collection_image_url": collection_logo
        #     }
        #
        #     logging.debug(payload)
        #     logging.debug(content_type)
        #     try:
        #         update = notify_email_multicast_default(
        #             payload_dict=payload,
        #             content_type=content_type
        #         )
        #     except Exception as e:
        #         raise e
        #
        #     if not update:
        #         logger.info("re-queuing send_notification_users_with_white_list")
        #         status = False

        return status


collection_service_cls = CollectionService()
