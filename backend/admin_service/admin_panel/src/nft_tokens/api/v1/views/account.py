from rest_framework.parsers import FormParser, MultiPartParser

from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
)
from nft_tokens.api.v1.views import base
from nft_tokens.models import Account
from nft_tokens.pagination import StandardResultsSetPagination
from nft_tokens.serializers import (
    AccountNotCountSerializer,
    AccountSerializer,
    HideAccountSerializer,
)


class AccountViewSet(base.CustomModelViewSet):
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]
    queryset = Account.objects.filter(hide=False)
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "create":
            return AccountNotCountSerializer
        if self.action == "update" or self.action == "partial_update":
            return AccountNotCountSerializer
        return AccountSerializer


class HideAccountView(base.UpdateView):
    queryset = Account.objects.filter(hide=False)
    serializer_class = HideAccountSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
