from django.db.models import Count, Min, Q, Sum

from nft_tokens.models import Account
from nft_tokens.services.base_service import BaseService


class AccountService(BaseService):
    model = Account
    list_params = [
        "collections_count",
        "items_count",
        "owners_count",
        "floor_price_count",
        "volume_troded_count",
        "profit",
    ]

    def get_template_params_update(self):
        self.template_params_update = {
            "collections_count": Count("collection__id", distinct=True),
            "items_count": Count("collection__token"),
            "owners_count": Count(
                "collection__token", filter=Q(collection__token__mint=True)
            ),
            "floor_price_count": Min("collection__token__price"),
            "volume_troded_count": Sum(
                "collection__token__price",
                filter=Q(collection__token__mint=True),
            ),
            "profit": Sum("collection__token__price"),
        }


account_service_cls = AccountService()
