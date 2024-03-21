import logging
from typing import List

from django import dispatch
from django.db.models import Count, Sum

from nft_tokens.models import Pack
from nft_tokens.services.base_service import BaseService

logger = logging.getLogger(__name__)

pack_update = dispatch.Signal()


class PackService(BaseService):
    model = Pack
    list_params = ["items_count", "profit"]

    def get_template_params_update(self):
        self.template_params_update = {
            "items_count": Count("token", distinct=True),
            "profit": Sum("token__price"),
        }

    def send_signal_pack_update(self, pack_id: str, update_fields: List[str]):
        pack_update.send(
            sender=self.__class__, pack_id=pack_id, update_fields=update_fields
        )


pack_service_cls = PackService()
