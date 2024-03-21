from rest_framework.parsers import FormParser, MultiPartParser

from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
)
from nft_tokens.api.v1.views import base
from nft_tokens.models import Page
from nft_tokens.serializers import (
    HidePageSerializer,
    PageListSerializer,
    PageSerializer,
)


class PageViewSet(base.CustomModelViewSet):
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]
    queryset = Page.objects.filter(hide=False).order_by("number")
    lookup_field = "url"
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут

    def get_serializer_class(self):
        if self.action == "list":
            return PageListSerializer
        return PageSerializer


class HidePageView(base.UpdateView):
    queryset = Page.objects.filter(hide=False)
    serializer_class = HidePageSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
