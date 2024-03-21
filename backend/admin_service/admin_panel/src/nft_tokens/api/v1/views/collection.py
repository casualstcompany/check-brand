from rest_framework import serializers

from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
)
from nft_tokens import filters
from nft_tokens.api.v1.views import base
from nft_tokens.constants import msg
from nft_tokens.models import Account, Collection, Page
from nft_tokens.pagination import StandardResultsSetPagination
from nft_tokens.serializers import (
    CollectionMiniSerializer,
    CollectionSerializer,
    CreateCollectionSerializer,
    HideCollectionSerializer,
    UpdateCollectionSerializer,
)
from nft_tokens.serializers.collection import StatusUpdateCollectionSerializer


class CollectionViewSet(base.CustomModelViewSet):
    queryset = (
        Collection.objects.select_related("blockchain")
        .prefetch_related("payment_tokens")
        .all()
    )
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCollectionSerializer
        if self.action == "update" or self.action == "partial_update":
            return UpdateCollectionSerializer
        return CollectionSerializer


class HideCollectionView(base.UpdateView):
    queryset = Collection.objects.filter(hide=False)
    serializer_class = HideCollectionSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут


class CollectionByPageView(base.ListView):
    http_method_names = ["get"]
    serializer_class = CollectionSerializer
    filter_backends = (
        filters.FilterByPageBackend,
        filters.FilterByRandomNumberBackend,
        filters.FilterByAccountBackend,
    )
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = {"hide": False}

        page_id = self.request.query_params.get("page_id")
        account_id = self.request.query_params.get("account_id")
        random_number = self.request.query_params.get("random_number")

        filters.filter_model_by_id(
            params=params,
            model_id=account_id,
            model_name_str="account",
            model=Account,
        )
        filters.filter_model_by_id(
            params=params, model_id=page_id, model_name_str="page", model=Page
        )

        queryset = Collection.objects.filter(**params)

        if random_number:
            try:
                random_number = int(random_number)
            except ValueError:
                raise serializers.ValidationError(
                    {"random_number": msg.random_number_not_integer}
                )
            queryset = queryset.order_by("?")[:random_number]

        return queryset


class CollectionMiniFilterListView(base.ListView):
    serializer_class = CollectionMiniSerializer
    filter_backends = (
        filters.FilterByPageBackend,
        filters.FilterByAccountBackend,
    )
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
    http_method_names = ["get"]

    def get_queryset(self):
        params = {"hide": False}

        page_id = self.request.query_params.get("page_id")
        account_id = self.request.query_params.get("account_id")

        filters.filter_model_by_id(
            params=params,
            model_id=account_id,
            model_name_str="account",
            model=Account,
        )
        filters.filter_model_by_id(
            params=params, model_id=page_id, model_name_str="page", model=Page
        )

        queryset = Collection.objects.filter(**params).values("id", "name")

        return queryset


class StatusUpdateCollectionView(base.UpdateView):
    """Ручка для управления статусами mint коллекции"""

    queryset = Collection.objects.filter(hide=False)
    serializer_class = StatusUpdateCollectionSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
