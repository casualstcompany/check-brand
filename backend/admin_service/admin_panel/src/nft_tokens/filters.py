import coreapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers

from nft_tokens import utils
from nft_tokens.constants import msg


def filter_model_by_id(params, model_id, model_name_str, model):
    if model_id is not None:
        if not utils.validate_uuid4(model_id):
            raise serializers.ValidationError(
                {
                    f"{model_name_str}_id": msg.model_not_exist.format(
                        model_name_str=model_name_str
                    )
                }
            )
        try:
            obj = model.objects.get(id=model_id, hide=False)
        except model.DoesNotExist:
            raise serializers.ValidationError(
                {
                    f"{model_name_str}_id": msg.model_not_exist.format(
                        model_name_str=model_name_str
                    )
                }
            )
        utils.set_if_value(params, model_name_str, obj)


class FilterByCollectionBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="collection_id",
                location="query",
                required=False,
                type="string",
            ),
        ]


class FilterByAccountBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="account_id",
                location="query",
                required=False,
                type="string",
            ),
        ]


class FilterByPackBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="pack_id", location="query", required=False, type="string"
            ),
        ]


class FilterByBlockchainBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="blockchain_id",
                location="query",
                required=False,
                type="string",
            ),
        ]


class FilterByRandomNumberBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="random_number",
                location="query",
                required=False,
                type="integer",
            ),
        ]


class FilterByPageBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="page_id", location="query", required=False, type="string"
            ),
        ]


class FilterByWalletOwnerBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="wallet_owner",
                location="query",
                required=False,
                type="string",
            )
        ]
