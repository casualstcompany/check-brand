import traceback
from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from nft_tokens.serializers.collection import ChildCollectionNameLogoSerializer

from .models import (
    ApplicationService,
    Company,
    Contacts,
    Cooperation,
    Service,
    UsedService,
)
from nft_tokens.models import Collection
from auth_by_grpc.utils import validate_is_admin


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"

    def validate_service(self, data):
        request = self.context.get("request")

        if validate_is_admin(request.user):
            return data

        if data.company.owner == request.user.user_wallet:
            return data

        raise serializers.ValidationError(
            detail=[
                "Компания сервиса не принадлежит авторизованному пользователю"
            ],
            code="company_not_found",
        )


class ChildCreateContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        exclude = ("service",)


class ChildUpdateContactsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Contacts
        exclude = ("service",)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ("status_moderator",)

    def validate_company(self, data):
        request = self.context.get("request")

        if validate_is_admin(request.user):
            return data

        if data.owner == request.user.user_wallet:
            return data

        raise serializers.ValidationError(
            detail=["Компания не принадлежит авторизованному пользователю"],
            code="company_not_found",
        )

    def get_used(self, obj):
        request = self.context.get("request")

        if request.user.is_authenticated:
            return obj.used.filter(owner=request.user.user_wallet).exists()
        return False


class PatchServiceSerializer(ServiceSerializer):
    """
    Only for schema generation, not actually used.
    because DRF-YASG does not support partial.
    """

    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = (
            "owner",
            "status_moderator",
        )

    def create(self, validated_data):
        serializers.raise_errors_on_nested_writes(
            "create", self, validated_data
        )
        model_class: Company = self.Meta.model
        request = self.context.get("request")

        info = model_meta.get_field_info(model_class)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = model_class._default_manager.create(
                **validated_data, owner=request.user.user_wallet
            )
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    model_class.__name__,
                    model_class._default_manager.name,
                    model_class.__name__,
                    model_class._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg)

            # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class PatchCompanySerializer(CompanySerializer):
    """
    Only for schema generation, not actually used.
    because DRF-YASG does not support partial.
    """

    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields


class RetrieveCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = ["id", "name", "logo"]


class RetrieveContactsSerializer(ContactsSerializer):
    class Meta:
        model = Contacts
        exclude = ("service", "created_at", "updated_at")


class ListServiceSerializer(ServiceSerializer):
    company = RetrieveCompanySerializer()
    contacts = RetrieveContactsSerializer(read_only=True, many=True)
    collections = ChildCollectionNameLogoSerializer(read_only=True, many=True)
    used = serializers.SerializerMethodField(read_only=True)


class DetailServiceSerializer(ServiceSerializer):
    company = RetrieveCompanySerializer()
    contacts = RetrieveContactsSerializer(read_only=True, many=True)
    collections = ChildCollectionNameLogoSerializer(read_only=True, many=True)
    used = serializers.SerializerMethodField(read_only=True)


class CreateServiceSerializer(ServiceSerializer):
    contacts = ChildCreateContactsSerializer(many=True)
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), many=True
    )

    class Meta:
        model = Service
        fields = (
            "id",
            "contacts",
            "type",
            "manager_telegram",
            "manager_whatsapp",
            "manager_email",
            "preview",
            "description",
            "company",
            "collections",
            "active",
            "status_moderator",
            "certificate_type",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status_moderator",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        contacts = validated_data.pop("contacts")
        collections = validated_data.pop("collections")

        raise_errors_on_nested_writes("create", self, validated_data)

        if not transaction.get_autocommit():
            raise RuntimeError("Не удалось загрузить сервис. Попробуй позже.")

        with transaction.atomic():
            instance = self.Meta.model._default_manager.create(
                **validated_data
            )

            for item in contacts:
                Contacts.objects.create(**item, service=instance)

            instance.collections.set(collections)

        validated_data["id"] = instance.id
        validated_data["contacts"] = instance.contacts
        validated_data["created_at"] = instance.created_at
        validated_data["updated_at"] = instance.updated_at
        validated_data["status_moderator"] = instance.status_moderator
        validated_data["collections"] = collections
        validated_data["certificate_type"] = instance.certificate_type

        return validated_data


class UpdateServiceSerializer(ServiceSerializer):
    contacts = ChildUpdateContactsSerializer(many=True)
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), many=True
    )

    class Meta:
        model = Service
        fields = (
            "id",
            "contacts",
            "type",
            "manager_telegram",
            "manager_whatsapp",
            "manager_email",
            "preview",
            "description",
            "company",
            "collections",
            "active",
            "status_moderator",
            "certificate_type",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status_moderator",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        contacts = validated_data.pop("contacts")

        raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)

        if not transaction.get_autocommit():
            raise RuntimeError("Не удалось обновить сервис. Попробуй позже.")

        with transaction.atomic():
            m2m_fields = []
            for attr, value in validated_data.items():
                if attr in info.relations and info.relations[attr].to_many:
                    m2m_fields.append((attr, value))
                else:
                    setattr(instance, attr, value)
            instance.save()

            for contact in contacts:
                contact_id = contact.pop("id", None)
                if contact_id:
                    Contacts.objects.filter(
                        id=contact_id, service=instance
                    ).update(**contact)
                else:
                    Contacts.objects.create(**contact, service=instance)

            for attr, value in m2m_fields:
                field = getattr(instance, attr)
                field.set(value)

        return instance


class BaseUsedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedService
        fields = (
            "id",
            "service",
            "token",
            "owner",
            "status",
        )
        read_only_fields = (
            "id",
            "owner",
            "status",
        )

    def validate_token(self, data):
        request = self.context.get("request")

        if validate_is_admin(request.user):
            return data

        if data.wallet_owner == request.user.user_wallet:
            return data

        if data.email == request.user.email:
            return data

        raise serializers.ValidationError(
            detail=["Сертификат не принадлежит пользователю"],
            code="token_not_found",
        )


class UsedServiceSerializer(BaseUsedServiceSerializer):
    def validate(self, attrs):
        if UsedService.objects.filter(
            service=attrs.get("service"),
            token=attrs.get("token"),
            status=UsedService.StatusUsedServiceChoices.USED,
        ).exists():
            raise serializers.ValidationError(
                detail=["Услуга с данным сертификатом уже была использована"],
                code="is_used",
            )
        return super().validate(attrs)

    def create(self, validated_data):
        serializers.raise_errors_on_nested_writes(
            "create", self, validated_data
        )
        request = self.context.get("request")

        try:
            instance = UsedService.objects.get(
                **validated_data,
            )
            instance.owner = request.user.user_wallet
            instance.status = UsedService.StatusUsedServiceChoices.USED
            instance.save()
        except UsedService.DoesNotExist:
            instance = UsedService.objects.create(
                **validated_data,
                owner=request.user.user_wallet,
                status=UsedService.StatusUsedServiceChoices.USED,
            )
        return instance


class СlickedServiceSerializer(BaseUsedServiceSerializer):
    def create(self, validated_data):
        serializers.raise_errors_on_nested_writes(
            "create", self, validated_data
        )
        request = self.context.get("request")

        try:
            instance = UsedService.objects.get(
                **validated_data,
            )
            if (
                (
                    instance.status
                    == UsedService.StatusUsedServiceChoices.CLICKED
                    and instance.owner != request.user.user_wallet
                )
                or instance.status
                == UsedService.StatusUsedServiceChoices.NOT_USED
            ):
                instance.owner = request.user.user_wallet
                instance.status = UsedService.StatusUsedServiceChoices.CLICKED
                instance.save()
        except UsedService.DoesNotExist:
            instance = UsedService.objects.create(
                **validated_data,
                owner=request.user.user_wallet,
                status=UsedService.StatusUsedServiceChoices.CLICKED,
            )
        return instance


class NotUsedServiceSerializer(BaseUsedServiceSerializer):
    def create(self, validated_data):
        serializers.raise_errors_on_nested_writes(
            "create", self, validated_data
        )
        request = self.context.get("request")

        try:
            instance = UsedService.objects.get(
                **validated_data,
            )
            if (
                instance.status == UsedService.StatusUsedServiceChoices.CLICKED
                or (
                    instance.status
                    == UsedService.StatusUsedServiceChoices.NOT_USED
                    and instance.owner != request.user.user_wallet
                )
            ):
                instance.owner = request.user.user_wallet
                instance.status = UsedService.StatusUsedServiceChoices.NOT_USED
                instance.save()
        except UsedService.DoesNotExist:
            instance = UsedService.objects.create(
                **validated_data,
                owner=request.user.user_wallet,
                status=UsedService.StatusUsedServiceChoices.NOT_USED,
            )
        return instance


class CooperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperation
        fields = [
            "email",
            "name",
            "phone",
            "site",
        ]


class PayloadApplicationSerializer(serializers.Serializer):
    telegram = serializers.CharField(required=False)
    whatsapp = serializers.CharField(required=False)


class ApplicationSerializer(serializers.ModelSerializer):
    payload = PayloadApplicationSerializer()

    class Meta:
        model = ApplicationService
        fields = [
            "service",
            "token",
            "payload",
        ]

    def validate_token(self, data):
        request = self.context.get("request")

        if validate_is_admin(request.user):
            return data

        if data.wallet_owner == request.user.user_wallet:
            return data

        if data.email == request.user.email:
            return data

        raise serializers.ValidationError(
            detail=["Сертификат не принадлежит пользователю"],
            code="token_not_found",
        )

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["owner"] = request.user.user_wallet
        validated_data["email"] = request.user.email

        return super().create(validated_data)
