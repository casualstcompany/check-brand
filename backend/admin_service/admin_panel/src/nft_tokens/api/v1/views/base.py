from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from auth_by_grpc.permission import (
    AdminOrUserGetGRPCPermission,
    OnlyAdminGRPCPermission,
)


class ErrorDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(required=False)


class BadRequestSerializer(serializers.Serializer):
    non_field_errors = serializers.ManyRelatedField(
        child_relation=serializers.CharField(required=False)
    )
    field_name = serializers.ManyRelatedField(
        child_relation=serializers.CharField(required=False)
    )


decorator_list = swagger_auto_schema(
    responses={
        401: ErrorDetailSerializer(),
        403: ErrorDetailSerializer(),
    }
)
decorator_create_update = swagger_auto_schema(
    responses={
        401: ErrorDetailSerializer(),
        403: ErrorDetailSerializer(),
        400: BadRequestSerializer(),
    }
)


@method_decorator(name="list", decorator=decorator_list)
@method_decorator(name="retrieve", decorator=decorator_list)
@method_decorator(name="create", decorator=decorator_create_update)
@method_decorator(name="partial_update", decorator=decorator_create_update)
@method_decorator(name="update", decorator=decorator_create_update)
class CreateUpdateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AdminOrUserGetGRPCPermission]


@method_decorator(name="list", decorator=decorator_create_update)
class ListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AdminOrUserGetGRPCPermission]


@method_decorator(name="update", decorator=decorator_create_update)
@method_decorator(name="partial_update", decorator=decorator_create_update)
class HideViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [OnlyAdminGRPCPermission]


@method_decorator(name="update", decorator=decorator_create_update)
@method_decorator(name="partial_update", decorator=decorator_create_update)
class UpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [OnlyAdminGRPCPermission]


@method_decorator(name="create", decorator=decorator_create_update)
class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [OnlyAdminGRPCPermission]


class CustomModelViewSet(ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"error": "some relation exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_destroy(self, instance):
        instance.hide = True
        instance.save()
