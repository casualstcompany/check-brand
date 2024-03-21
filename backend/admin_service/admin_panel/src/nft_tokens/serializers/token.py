import decimal
import logging
from typing import List

import requests
from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from nft_tokens import constants, utils
from nft_tokens.constants import msg
from nft_tokens.models import (
    CreatorRoyaltyDistribution,
    IncomeDistribution,
    LevelsStats,
    Properties,
    Token,
)
from nft_tokens.serializers.collection import CollectionForTokenSerializer
from nft_tokens.serializers.extra import (
    CreatorRoyaltyDistributionSerializer,
    IncomeDistributionSerializer,
    LevelsStatsSerializer,
    PropertiesSerializer,
)
from nft_tokens.serializers.pack import (
    BaseUpdatePackTokenMixin,
    GetM2MPackSerializer,
    PackForTokenSerializer,
)
from nft_tokens.services import PreSignedUrlS3StorageService

logger = logging.getLogger(__name__)
PATH_TOKEN_FILES = "collections/{collection}/{pack}/tokens/"
PREVIEW = "preview/"


class TokenUpdateCreateMixin:
    class Meta:
        model = Token

    @staticmethod
    def validate_file_1_name_ext(value):
        if not utils.validate_extension(
            file_name=value, allowed_extensions=constants.FILE_EXTENSION
        ):
            raise serializers.ValidationError([msg.allowed_extension_file])
        return value

    @staticmethod
    def validate_file_2_name_ext(value):
        if not utils.validate_extension(
            file_name=value, allowed_extensions=constants.FILE_EXTENSION
        ):
            raise serializers.ValidationError([msg.allowed_extension_file])
        return value

    def check_exists_duplicate_name(self, name, collection, token_id=None):
        duplicate = self.Meta.model.objects.filter(
            name=name, collection=collection
        )
        if duplicate.exists() and duplicate[0].id != token_id:
            raise serializers.ValidationError(
                {"name": [msg.error_collection_name_unique]}
            )

    @staticmethod
    def generate_path_and_uuid_name_for_files(
        collection, pack, validated_data
    ):
        path = PATH_TOKEN_FILES.format(collection=collection, pack=pack)
        if validated_data.get("file_1_name_ext"):
            validated_data["file_1_name_ext"] = utils.file_generate_name_uuid(
                validated_data["file_1_name_ext"], path=path
            )
        if validated_data.get("file_2_name_ext"):
            validated_data["file_2_name_ext"] = utils.file_generate_name_uuid(
                validated_data["file_2_name_ext"], path=path + PREVIEW
            )

    @staticmethod
    def output_transformation_validated_data(validated_data, instance):
        validated_data["id"] = instance.id
        pre_signed_url_service = PreSignedUrlS3StorageService()
        if validated_data.get("file_1_name_ext"):
            validated_data["file_1_pre_signed_url_data"] = (
                pre_signed_url_service.execute(
                    filename=instance.file_1_name_ext
                )
            )

        if validated_data.get("file_2_name_ext"):
            validated_data["file_2_pre_signed_url_data"] = (
                pre_signed_url_service.execute(
                    filename=instance.file_2_name_ext
                )
            )

        validated_data["creator_royalty_distribution"] = (
            instance.creator_royalty_distribution
        )
        validated_data["income_distribution"] = instance.income_distribution
        validated_data["properties"] = instance.properties
        validated_data["levels_stats"] = instance.levels_stats


class BaseTokenSerializer(serializers.ModelSerializer):
    wallet_owner = serializers.CharField(read_only=True)
    hide = serializers.BooleanField(read_only=True)
    mint = serializers.BooleanField(read_only=True)
    paid = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)
    upload_blockchain = serializers.BooleanField(read_only=True)
    freeze = serializers.BooleanField(read_only=True)
    profit = serializers.DecimalField(
        read_only=True, decimal_places=8, max_digits=15
    )

    creator_royalty_distribution = CreatorRoyaltyDistributionSerializer(
        many=True, read_only=True
    )
    income_distribution = IncomeDistributionSerializer(
        many=True, read_only=True
    )
    properties = PropertiesSerializer(many=True, read_only=True)
    levels_stats = LevelsStatsSerializer(many=True, read_only=True)
    collection = CollectionForTokenSerializer(read_only=True)
    pack = PackForTokenSerializer(read_only=True)

    class Meta:
        model = Token
        exclude = ["created_at", "updated_at"]

    @staticmethod
    def get_coefficient_to_usd(key_1, key_2):
        coefficient = cache.get(f"{key_1}-{key_2}")
        logger.info(f"coefficient-{coefficient}")
        if not coefficient:
            i = 0
            for a in range(10):
                # TODO вынести путь в конфиг
                response = requests.get(
                    f"https://min-api.cryptocompare.com/data/price?fsym={key_1}&tsyms={key_2}"
                )
                if response.status_code == 200:
                    response = response.json()
                    coefficient = decimal.Decimal(response.get(f"{key_2}"))
                    break
                i += 1
                if i > 10:
                    coefficient = 0
                    break
            cache.set(f"{key_1}-{key_2}", coefficient, 120)
        return coefficient

    def get_price_in_usd(self, obj):
        coefficient = self.get_coefficient_to_usd(key_1="ETH", key_2="USD")
        price_in_usd = round(obj.price * coefficient, 2)
        return str(price_in_usd)


class TokenSerializer(BaseTokenSerializer):
    price_in_usd = serializers.SerializerMethodField(read_only=True)


class TokenNotFileSerializer(BaseTokenSerializer):
    wallet_owner = serializers.CharField(read_only=True)
    hide = serializers.BooleanField(read_only=True)
    mint = serializers.BooleanField(read_only=True)
    paid = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)
    upload_blockchain = serializers.BooleanField(read_only=True)
    freeze = serializers.BooleanField(read_only=True)
    profit = serializers.DecimalField(
        read_only=True, decimal_places=8, max_digits=15
    )
    price_in_usd = serializers.CharField(read_only=True, default="0")

    class Meta:
        model = Token
        exclude = [
            "close_image",
            "file_1",
            "file_2",
            "created_at",
            "updated_at",
        ]


class UpdateTokenSerializer(
    TokenUpdateCreateMixin, BaseUpdatePackTokenMixin, BaseTokenSerializer
):
    id = serializers.UUIDField(read_only=True)

    creator_royalty_distribution = CreatorRoyaltyDistributionSerializer(
        many=True, required=False
    )
    income_distribution = IncomeDistributionSerializer(
        many=True, required=False
    )
    levels_stats = LevelsStatsSerializer(many=True, required=False)
    properties = PropertiesSerializer(many=True, required=False)

    file_1_name_ext = serializers.CharField(required=False)
    file_2_name_ext = serializers.CharField(required=False)
    file_1_pre_signed_url_data = serializers.CharField(read_only=True)
    file_2_pre_signed_url_data = serializers.CharField(read_only=True)

    class Meta:
        model = Token
        fields = [
            "id",
            "pack",
            "file_1_name_ext",
            "file_2_name_ext",
            "name",
            "price",
            "block",
            "status_price",
            "description",
            "unlockable",
            "unlockable_content",
            "creator_royalty_distribution",
            "income_distribution",
            "properties",
            "levels_stats",
            "currency_token",
            "investor_royalty",
            "creator_royalty",
            "file_1_pre_signed_url_data",
            "file_2_pre_signed_url_data",
        ]

    def validate(self, validated_data):
        instance = getattr(self, "instance", None)

        if (
            instance.block
            and validated_data.get("block")
            or instance.block
            and validated_data.get("block") is not False
        ):
            raise serializers.ValidationError(
                {"block": [msg.data_editing_blocked]}
            )

        name_token = validated_data.get("name")

        if name_token:
            self.check_exists_duplicate_name(
                name=name_token,
                collection=instance.collection,
                token_id=instance.id,
            )

        utils.base_validate_create_update_pack_token(
            data=validated_data, instance=instance
        )

        return validated_data

    def update(self, instance, validated_data):
        self.generate_path_and_uuid_name_for_files(
            collection=instance.collection.id,
            pack=instance.pack.id,
            validated_data=validated_data,
        )
        self.base_update_pack_token(
            instance=instance, validated_data=validated_data
        )
        self.output_transformation_validated_data(
            validated_data=validated_data, instance=instance
        )

        for attr in [
            "name",
            "price",
            "description",
            "currency_token",
            "investor_royalty",
            "creator_royalty",
        ]:
            if not validated_data.get(attr):
                validated_data[attr] = getattr(instance, attr)

        return validated_data


class HideTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["hide"]


class TokenConfirmationUploadFileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    file_1_name_ext = serializers.CharField(required=False)
    file_2_name_ext = serializers.CharField(required=False)

    class Meta:
        model = Token
        fields = ["id", "file_1_name_ext", "file_2_name_ext"]

    def update(self, instance, validated_data):
        file_1_name_ext = validated_data.get("file_1_name_ext")
        file_2_name_ext = validated_data.get("file_2_name_ext")

        if file_1_name_ext:
            if file_1_name_ext != instance.file_1_name_ext:
                raise serializers.ValidationError(
                    {"file_1_name_ext": [msg.does_not_match_the_existing_one]}
                )

            instance.file_1 = instance.file_1.field.attr_class(
                instance, instance.file_1.field, instance.file_1_name_ext
            )

        if file_2_name_ext:
            if file_2_name_ext != instance.file_2_name_ext:
                raise serializers.ValidationError(
                    {"file_2_name_ext": [msg.does_not_match_the_existing_one]}
                )
            instance.file_2 = instance.file_2.field.attr_class(
                instance, instance.file_2.field, instance.file_2_name_ext
            )

        instance.save()

        return validated_data


class TokenByPackSerializer(
    serializers.ModelSerializer, TokenUpdateCreateMixin
):
    id = serializers.UUIDField(read_only=True)

    file_1_name_ext = serializers.CharField(required=False)
    file_2_name_ext = serializers.CharField(required=True)
    file_1_pre_signed_url_data = serializers.CharField(read_only=True)
    file_2_pre_signed_url_data = serializers.CharField(read_only=True)

    description = serializers.CharField(required=False)

    creator_royalty_distribution = CreatorRoyaltyDistributionSerializer(
        many=True, required=False
    )
    income_distribution = IncomeDistributionSerializer(
        many=True, required=False
    )
    levels_stats = LevelsStatsSerializer(many=True, required=False)
    properties = PropertiesSerializer(many=True, required=False)

    class Meta:
        model = Token
        fields = [
            "id",
            "pack",
            "file_1_name_ext",
            "file_2_name_ext",
            "name",
            "price",
            "status_price",
            "description",
            "unlockable",
            "unlockable_content",
            "creator_royalty_distribution",
            "income_distribution",
            "properties",
            "levels_stats",
            "currency_token",
            "investor_royalty",
            "creator_royalty",
            "file_1_pre_signed_url_data",
            "file_2_pre_signed_url_data",
        ]

    @staticmethod
    def _set_params_from_pack(params: dict, pack) -> None:
        utils.set_if_value(params, "collection", pack.collection)
        utils.set_if_value(params, "type", pack.type)
        utils.set_if_value(params, "status", pack.status)
        if not params.get("status_price"):
            utils.set_if_value(params, "status_price", pack.status_price)
        if not params.get("description"):
            utils.set_if_value(params, "description", pack.description)
        if not params.get("close"):
            utils.set_if_value(params, "close", pack.close)
        if not params.get("close_image"):
            utils.set_if_value(params, "close_image", pack.close_image)
        if not params.get("unlockable"):
            utils.set_if_value(params, "unlockable", pack.unlockable)
        if not params.get("unlockable_content"):
            utils.set_if_value(
                params, "unlockable_content", pack.unlockable_content
            )

    @staticmethod
    def set_m2m_from_validate_data(
        update_data: List,
        pack_dict: dict,
        filed_name: str,
        model_m2m,
        instance,
        valid_exists=False,
    ):
        if update_data:
            utils.create_and_add_m2m(
                model_m2m,
                getattr(instance, filed_name),
                update_data,
                valid_exists,
            )
            pack_dict.pop(filed_name, None)

    def validate(self, validated_data):
        pack = validated_data.get("pack")
        name_token = validated_data.get("name")

        collection_token = pack.collection

        self.check_exists_duplicate_name(
            name=name_token, collection=collection_token
        )

        utils.base_validate_create_update_pack_token(
            data=validated_data, instance=pack
        )

        return validated_data

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

        pack = validated_data.get("pack")
        self._set_params_from_pack(validated_data, pack)
        pack_dict = GetM2MPackSerializer(pack).data

        raise_errors_on_nested_writes("create", self, validated_data)

        self.generate_path_and_uuid_name_for_files(
            collection=validated_data["collection"],
            pack=validated_data["pack"],
            validated_data=validated_data,
        )

        if not transaction.get_autocommit():
            raise RuntimeError(msg.error_later_load)

        with transaction.atomic():
            instance = self.Meta.model._default_manager.create(
                **validated_data
            )
            # wallet_owner=request.user.user_wallet

            self.set_m2m_from_validate_data(
                update_data=creator_royalty_distribution,
                pack_dict=pack_dict,
                filed_name="creator_royalty_distribution",
                model_m2m=CreatorRoyaltyDistribution,
                instance=instance,
                valid_exists=True,
            )

            self.set_m2m_from_validate_data(
                update_data=income_distribution,
                pack_dict=pack_dict,
                filed_name="income_distribution",
                model_m2m=IncomeDistribution,
                instance=instance,
                valid_exists=True,
            )

            self.set_m2m_from_validate_data(
                update_data=properties,
                pack_dict=pack_dict,
                filed_name="properties",
                model_m2m=Properties,
                instance=instance,
                valid_exists=True,
            )

            self.set_m2m_from_validate_data(
                update_data=levels_stats,
                pack_dict=pack_dict,
                filed_name="levels_stats",
                model_m2m=LevelsStats,
                instance=instance,
                valid_exists=True,
            )

            utils.set_m2m_from_dict_to_instance(pack_dict, instance)

        self.output_transformation_validated_data(
            validated_data=validated_data, instance=instance
        )

        return validated_data


class TokenByCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["collection"]
