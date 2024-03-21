from rest_framework import serializers

from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
    OnlyAuthorizedUserGRPCPermission,
)
from nft_tokens import filters, utils
from nft_tokens.api.v1.views import base
from nft_tokens.constants import msg
from nft_tokens.models import Collection, Pack, Token
from nft_tokens.pagination import StandardResultsSetPagination
from nft_tokens.serializers import (
    HideTokenSerializer,
    TokenByPackSerializer,
    TokenConfirmationUploadFileSerializer,
    TokenNotFileSerializer,
    TokenSerializer,
    UpdateTokenSerializer,
)


class TokenByPackViewSet(base.CreateViewSet):
    serializer_class = TokenByPackSerializer
    http_method_names = ["post"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут


class TokenUserView(base.ListView):
    http_method_names = ["get"]
    permission_classes = [OnlyAuthorizedUserGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return TokenSerializer
        return TokenSerializer

    def get_queryset(self):
        params = {
            "hide": False,
            "paid": True,
        }

        if self.request.user.email != "":
            params["email"] = self.request.user.email

        queryset = (
            Token.objects.filter(**params)
            .select_related("collection", "pack")
            .prefetch_related(
                "properties",
                "levels_stats",
                "creator_royalty_distribution",
                "income_distribution",
            )
        )
        return queryset


class TokenViewSet(base.CustomModelViewSet):
    http_method_names = ["patch", "put", "get", "delete"]
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return UpdateTokenSerializer
        if self.action == "list":
            return TokenSerializer
        return TokenSerializer

    def get_queryset(self):
        params = {"hide": False}

        if self.action == "update" or self.action == "partial_update":
            params["paid"] = False
            params["mint"] = False

        if self.action == "destroy":
            params["paid"] = False
            params["mint"] = False
            params["block"] = False

        queryset = Token.objects.filter(**params)
        return queryset


class TokenNotFileView(base.CustomModelViewSet):
    queryset = Token.objects.filter(hide=False)
    http_method_names = ["get"]
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    serializer_class = TokenNotFileSerializer


class HideTokenView(base.UpdateView):
    queryset = Token.objects.filter(hide=False, mint=False, paid=False)
    serializer_class = HideTokenSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут


class TokenByCollectionView(base.ListView):
    http_method_names = ["get"]
    serializer_class = TokenSerializer
    filter_backends = (
        filters.FilterByCollectionBackend,
        filters.FilterByPackBackend,
        filters.FilterByRandomNumberBackend,
        filters.FilterByWalletOwnerBackend,
    )
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = {"hide": False}

        collection_id = self.request.query_params.get("collection_id")
        pack_id = self.request.query_params.get("pack_id")
        wallet_owner = self.request.query_params.get("wallet_owner")
        random_number = self.request.query_params.get("random_number")

        filters.filter_model_by_id(
            params=params,
            model_id=collection_id,
            model_name_str="collection",
            model=Collection,
        )
        filters.filter_model_by_id(
            params=params, model_id=pack_id, model_name_str="pack", model=Pack
        )

        if wallet_owner is not None:
            utils.set_if_value(params, "wallet_owner", wallet_owner)

        queryset = Token.objects.filter(**params)

        if random_number:
            try:
                random_number = int(random_number)
            except ValueError:
                raise serializers.ValidationError(
                    {"random_number": msg.random_number_not_integer}
                )
            queryset = queryset.order_by("?")[:random_number]

        return queryset


class TokenConfirmationUploadFileView(base.UpdateView):
    queryset = Token.objects.filter(hide=False)
    serializer_class = TokenConfirmationUploadFileSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
