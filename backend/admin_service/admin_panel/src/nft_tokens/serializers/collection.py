from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from slugify import slugify

from nft_tokens.constants import msg
from nft_tokens.models import Collection, StatusToken
from nft_tokens.serializers.extra import (
    BlockchainSerializer,
    CurrencyTokenSerializer,
)
from nft_tokens.services.collection_service import collection_service_cls
from nft_tokens.utils import random_name, random_number


class CollectionSerializer(serializers.ModelSerializer):
    payment_tokens = CurrencyTokenSerializer(many=True, read_only=True)
    blockchain = BlockchainSerializer(read_only=True)

    class Meta:
        model = Collection
        exclude = ["updated_at"]


class CollectionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name"]

class ChildCollectionNameLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "logo"]


class BaseCreateUpdateCollectionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Collection
        exclude = [
            "created_at",
            "updated_at",
            "upload_blockchain",
            "items_count",
            "owners_count",
            "floor_price_count",
            "volume_troded_count",
            "creator_profit",
            "creator_fee",
            "profit",
        ]

    def validate_payment_tokens(self, value):
        blockchain = self.initial_data.get("blockchain")

        if not blockchain:
            instance = getattr(self, "instance", None)
            blockchain = str(instance.blockchain.id)

        for token in value:
            if str(token.blockchain.id) != blockchain:
                raise serializers.ValidationError(
                    msg.error_blockchain_not_collection
                )
        return value

    def validate_account(self, value):
        page = self.initial_data.get("page")

        if not page:
            instance = getattr(self, "instance", None)
            page = str(instance.page.id)

        if str(value.page.id) != page:
            raise serializers.ValidationError(
                msg.error_account_not_collection_page
            )
        return value


class CreateCollectionSerializer(BaseCreateUpdateCollectionSerializer):
    url = serializers.CharField(required=False)
    symbol = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get("url"):
            url = slugify(data.get("name"))
            while Collection.objects.filter(url=url).exists():
                url += random_name(2)
            data["url"] = url

        if not data.get("symbol"):
            symbol = "CBC" + random_number(3)
            while Collection.objects.filter(symbol=symbol).exists():
                symbol = "CBC" + random_number(3)
            data["symbol"] = symbol

        return data


class UpdateCollectionSerializer(BaseCreateUpdateCollectionSerializer):
    def validate_blockchain(self, value):
        payment_tokens = self.initial_data.get("payment_tokens")

        if not payment_tokens:
            instance = getattr(self, "instance", None)
            payment_tokens = instance.payment_tokens.all()

            for token in payment_tokens:
                if str(token.blockchain.id) != str(value):
                    raise serializers.ValidationError(
                        msg.error_blockchain_not_collection
                    )
        return value

    def validate_page(self, value):
        account = self.initial_data.get("account")

        if not account:
            instance = getattr(self, "instance", None)
            account = instance.account

            if str(account.page.id) != str(value):
                raise serializers.ValidationError(
                    msg.error_account_not_collection_page
                )
        return value


class HideCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["hide"]


class CollectionForTokenSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "name"]


class StatusUpdateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["status"]

    @staticmethod
    def status_queue_check(new_status: StatusToken, old_status: StatusToken):
        """В этом методе устанавливается и проверяется очередь, по которой идёт этапа минта."""
        execution_rules = {
            StatusToken.stop: [
                StatusToken.mint_1,
                StatusToken.mint_2,
                StatusToken.sold_out,
            ],
            StatusToken.book: [StatusToken.stop],
            StatusToken.mint_1: [StatusToken.book],
            StatusToken.mint_2: [StatusToken.mint_1],
            StatusToken.sold_out: [StatusToken.mint_1, StatusToken.mint_2],
        }
        if old_status not in execution_rules.get(new_status):
            raise serializers.ValidationError(
                msg.status_queue_broken
                % (
                    new_status,
                    [i.value for i in execution_rules.get(new_status)],
                )
            )

    def validate_status(self, value):
        instance = getattr(self, "instance", None)

        self.status_queue_check(new_status=value, old_status=instance.status)

        return value

    def update(self, instance, validated_data):
        """Метод дублируется только из того что нам необходимо вставить в конце свой сигнал."""
        raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        collection_service_cls.send_signal_status_update_in_collection(
            collection_id=instance.id
        )

        return instance
