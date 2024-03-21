import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from nft_tokens import utils
from nft_tokens.constants import msg
from nft_tokens.models import (
    CreatorRoyaltyDistribution,
    IncomeDistribution,
    LevelsStats,
    Pack,
    Properties,
)
from nft_tokens.serializers import base
from nft_tokens.serializers.extra import (
    CreatorRoyaltyDistributionSerializer,
    IncomeDistributionSerializer,
    LevelsStatsSerializer,
    PropertiesSerializer,
)
from nft_tokens.services.pack_service import pack_service_cls

logger = logging.getLogger(__name__)


class BaseUpdatePackTokenMixin:
    def base_update_pack_token(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        creator_royalty_distribution = utils.get_list_by_field(
            validated_data, "creator_royalty_distribution"
        )
        income_distribution = utils.get_list_by_field(
            validated_data, "income_distribution"
        )
        properties = utils.get_list_by_field(validated_data, "properties")
        levels_stats = utils.get_list_by_field(validated_data, "levels_stats")

        raise_errors_on_nested_writes("update", self, validated_data)

        if not transaction.get_autocommit():
            raise RuntimeError(msg.error_later_load)

        with transaction.atomic():
            for attr, value in validated_data.items():
                if attr in info.relations and info.relations[attr].to_many:
                    logger.info(f"attr-{attr}, value-{value}")
                else:
                    setattr(instance, attr, value)

            instance.save()
            utils.create_and_add_m2m(
                CreatorRoyaltyDistribution,
                instance.creator_royalty_distribution,
                creator_royalty_distribution,
                clear=True,
            )
            utils.create_and_add_m2m(
                IncomeDistribution,
                instance.income_distribution,
                income_distribution,
                clear=True,
            )
            utils.create_and_add_m2m(
                Properties,
                instance.properties,
                properties,
                valid_exists=True,
                clear=True,
            )
            utils.create_and_add_m2m(
                LevelsStats,
                instance.levels_stats,
                levels_stats,
                valid_exists=True,
                clear=True,
            )


class BaseCreateUpdatePackSerializer(
    serializers.ModelSerializer, BaseUpdatePackTokenMixin
):
    status = serializers.CharField(read_only=True)
    creator_royalty_distribution = CreatorRoyaltyDistributionSerializer(
        many=True, required=False
    )
    income_distribution = IncomeDistributionSerializer(
        many=True, required=False
    )
    levels_stats = LevelsStatsSerializer(many=True, required=False)
    properties = PropertiesSerializer(many=True, required=False)

    wallet_owner = serializers.CharField(read_only=True)
    close_image = base.Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    hide = serializers.BooleanField(read_only=True)
    upload_blockchain = serializers.BooleanField(read_only=True)
    freeze = serializers.BooleanField(read_only=True)

    items_count = serializers.DecimalField(
        read_only=True, decimal_places=8, max_digits=15
    )
    profit = serializers.DecimalField(
        read_only=True, decimal_places=8, max_digits=15
    )

    class Meta:
        model = Pack
        exclude = [
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        instance = getattr(self, "instance", None)
        utils.base_validate_create_update_pack_token(
            data=data, instance=instance
        )
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        creator_royalty_distribution = utils.get_list_by_field(
            validated_data, "creator_royalty_distribution"
        )
        income_distribution = utils.get_list_by_field(
            validated_data, "income_distribution"
        )
        properties = utils.get_list_by_field(validated_data, "properties")
        levels_stats = utils.get_list_by_field(validated_data, "levels_stats")

        if not transaction.get_autocommit():
            raise RuntimeError(msg.error_later_load)

        with transaction.atomic():
            pack = Pack.objects.create(
                **validated_data,
            )
            # wallet_owner=request.user.user_wallet
            utils.create_and_add_m2m(
                CreatorRoyaltyDistribution,
                pack.creator_royalty_distribution,
                creator_royalty_distribution,
            )
            utils.create_and_add_m2m(
                IncomeDistribution,
                pack.income_distribution,
                income_distribution,
            )
            utils.create_and_add_m2m(
                Properties, pack.properties, properties, valid_exists=True
            )
            utils.create_and_add_m2m(
                LevelsStats, pack.levels_stats, levels_stats, valid_exists=True
            )

        return pack

    def update(self, instance, validated_data):
        self.base_update_pack_token(
            instance=instance, validated_data=validated_data
        )
        update_fields = list(validated_data.keys())
        if update_fields != ["block"]:
            pack_service_cls.send_signal_pack_update(
                pack_id=instance.id, update_fields=list(validated_data.keys())
            )
        return instance


class CreatePackSerializer(BaseCreateUpdatePackSerializer):
    class Meta:
        model = Pack
        exclude = ["created_at", "updated_at"]


class UpdatePackSerializer(BaseCreateUpdatePackSerializer):
    class Meta:
        model = Pack
        exclude = ["created_at", "updated_at"]

    def validate(self, data):
        instance = getattr(self, "instance", None)

        if (
            instance.block
            and data.get("block")
            or instance.block
            and data.get("block") is not False
        ):
            raise serializers.ValidationError(
                {"block": [msg.data_editing_blocked]}
            )

        utils.base_validate_create_update_pack_token(
            data=data, instance=instance
        )
        return data


class RetrievePackSerializer(BaseCreateUpdatePackSerializer):
    wallet_owner = serializers.CharField(read_only=True)
    creator_royalty_distribution = CreatorRoyaltyDistributionSerializer(
        many=True, read_only=True
    )
    income_distribution = IncomeDistributionSerializer(
        many=True, read_only=True
    )
    properties = PropertiesSerializer(many=True, read_only=True)
    levels_stats = LevelsStatsSerializer(many=True, read_only=True)


class HidePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = ["hide"]


class ListRetrievePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        exclude = ["created_at", "updated_at"]


class GetM2MPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = [
            "creator_royalty_distribution",
            "income_distribution",
            "properties",
            "levels_stats",
        ]


class PackForTokenSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Pack
        fields = ["id", "name"]
