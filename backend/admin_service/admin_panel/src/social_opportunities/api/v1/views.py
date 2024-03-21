from rest_framework import viewsets, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from social_opportunities.filters import ServiceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from nft_tokens.pagination import StandardResultsSetPagination
from auth_by_grpc.permission import (
    OnlyAuthorizedUserGRPCPermission,
    OwnerOrAdminGRPCPermission,
)
from social_opportunities.models import (
    ApplicationService,
    Company,
    Contacts,
    Service,
    UsedService,
    Cooperation,
)
from social_opportunities.permission import (
    OwnerCompanyOrAdminGRPCPermission,
    OwnerCompanyServiceOrAdminGRPCPermission,
)
from social_opportunities.serializers import (
    ApplicationSerializer,
    CompanySerializer,
    ContactsSerializer,
    ServiceSerializer,
    PatchCompanySerializer,
    PatchServiceSerializer,
    ListServiceSerializer,
    CreateServiceSerializer,
    UpdateServiceSerializer,
    DetailServiceSerializer,
    UsedServiceSerializer,
    СlickedServiceSerializer,
    NotUsedServiceSerializer,
    CooperationSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [OnlyAuthorizedUserGRPCPermission]

        elif self.action == "retrieve":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "list":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "update":
            self.permission_classes = [OwnerOrAdminGRPCPermission]

        elif self.action == "partial_update":
            self.permission_classes = [OwnerOrAdminGRPCPermission]

        elif self.action == "destroy":
            self.permission_classes = [OwnerOrAdminGRPCPermission]

        return super().get_permissions()

    @swagger_auto_schema(request_body=PatchCompanySerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = (
        Service.objects.prefetch_related("contacts")
        .prefetch_related("collections")
        .select_related("company")
        .all()
    )
    serializer_class = ServiceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = ServiceFilter

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [OnlyAuthorizedUserGRPCPermission]

        elif self.action == "retrieve":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "list":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "update":
            self.permission_classes = [OwnerCompanyOrAdminGRPCPermission]

        elif self.action == "partial_update":
            self.permission_classes = [OwnerCompanyOrAdminGRPCPermission]

        elif self.action == "destroy":
            self.permission_classes = [OwnerCompanyOrAdminGRPCPermission]

        return super().get_permissions()

    def get_serializer_class(self):

        if self.action == "retrieve":
            return DetailServiceSerializer

        if self.action == "list":
            return ListServiceSerializer

        if self.action == "create":
            return CreateServiceSerializer

        if self.action in ["update", "partial_update"]:
            return UpdateServiceSerializer

        return super().get_serializer_class()

    @swagger_auto_schema(request_body=PatchServiceSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [OnlyAuthorizedUserGRPCPermission]

        elif self.action == "retrieve":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "list":
            self.permission_classes = [permissions.AllowAny]

        elif self.action == "update":
            self.permission_classes = [
                OwnerCompanyServiceOrAdminGRPCPermission
            ]

        elif self.action == "partial_update":
            self.permission_classes = [
                OwnerCompanyServiceOrAdminGRPCPermission
            ]

        elif self.action == "destroy":
            self.permission_classes = [
                OwnerCompanyServiceOrAdminGRPCPermission
            ]

        return super().get_permissions()


class UsedServiceViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UsedServiceSerializer
    queryset = UsedService.objects.all()

    def get_queryset(self):
        queryset = UsedService.objects.filter(
            owner=self.request.user.user_wallet
        )
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [OnlyAuthorizedUserGRPCPermission]

        elif self.action == "retrieve":
            self.permission_classes = [OwnerOrAdminGRPCPermission]

        elif self.action == "list":
            self.permission_classes = [OwnerOrAdminGRPCPermission]

        return super().get_permissions()


class СlickedServiceViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = СlickedServiceSerializer
    queryset = UsedService.objects.all()
    permission_classes = [OnlyAuthorizedUserGRPCPermission]


class NotUsedServiceViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotUsedServiceSerializer
    queryset = UsedService.objects.all()
    permission_classes = [OnlyAuthorizedUserGRPCPermission]


class CooperationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CooperationSerializer
    queryset = Cooperation.objects.all()
    permission_classes = [permissions.AllowAny]


class ApplicationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ApplicationSerializer
    queryset = ApplicationService.objects.all()
    permission_classes = [OnlyAuthorizedUserGRPCPermission]
