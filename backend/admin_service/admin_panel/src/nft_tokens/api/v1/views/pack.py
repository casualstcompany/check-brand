from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
)
from nft_tokens import filters
from nft_tokens.api.v1.views import base
from nft_tokens.models import Collection, Pack
from nft_tokens.pagination import StandardResultsSetPagination
from nft_tokens.serializers import (
    CreatePackSerializer,
    HidePackSerializer,
    ListRetrievePackSerializer,
    RetrievePackSerializer,
    UpdatePackSerializer,
)


class PackViewSet(base.CustomModelViewSet):
    queryset = Pack.objects.filter(hide=False)
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePackSerializer
        if self.action == "update" or self.action == "partial_update":
            return UpdatePackSerializer
        if self.action == "list":
            return ListRetrievePackSerializer
        return RetrievePackSerializer

    def get_queryset(self):
        if self.action == "destroy":
            self.queryset = Pack.objects.filter(block=False)

        return self.queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        self.action = "retrieve"
        return self.retrieve(self.request)


class HidePackViewSet(base.UpdateView):
    queryset = Pack.objects.filter(hide=False)
    serializer_class = HidePackSerializer
    http_method_names = ["patch"]
    permission_classes = [OnlyAdminGRPCPermission]  # TODO: тут


# TODO: Нужно ? (закомментировал 2.05.2023)
# class RoyaltyDistributionPackViewSet(base.UpdateView):
#
#     queryset = Pack.objects.filter(hide=False)
#     serializer_class = RoyaltyDistributionPackSerializer
#     http_method_names = ["patch"]
#     permission_classes = [OnlyAdminGRPCPermission]

# TODO: Нужно ? (закомментировал 2.05.2023)
# class IncomePackViewSet(base.UpdateView):
#
#     queryset = Pack.objects.filter(hide=False)
#     serializer_class = IncomeDistributionPackSerializer
#     http_method_names = ["patch"]
#     permission_classes = [OnlyAdminGRPCPermission]


class PackByCollectionView(base.ListView):
    http_method_names = ["get"]
    serializer_class = ListRetrievePackSerializer
    filter_backends = (filters.FilterByCollectionBackend,)
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = {"hide": False}

        collection_id = self.request.query_params.get("collection_id")

        filters.filter_model_by_id(
            params=params,
            model_id=collection_id,
            model_name_str="collection",
            model=Collection,
        )

        queryset = Pack.objects.filter(**params)

        return queryset
