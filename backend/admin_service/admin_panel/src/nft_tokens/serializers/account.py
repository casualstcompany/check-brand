from rest_framework import serializers

from nft_tokens.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["created_at", "updated_at"]


class AccountNotCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = [
            "created_at",
            "updated_at",
            "items_count",
            "owners_count",
            "collections_count",
            "floor_price_count",
            "volume_troded_count",
            "profit",
        ]


class HideAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["hide"]
