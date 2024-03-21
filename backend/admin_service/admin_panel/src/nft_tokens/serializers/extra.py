from rest_framework import serializers

from nft_tokens.models import (
    Blockchain,
    CreatorRoyaltyDistribution,
    CurrencyToken,
    IncomeDistribution,
    LevelsStats,
    Properties,
)


class LevelsStatsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = LevelsStats
        exclude = ["created_at", "updated_at"]


class PropertiesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Properties
        exclude = ["created_at", "updated_at"]


class CurrencyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyToken
        exclude = ["created_at", "updated_at"]


class CreateCurrencyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyToken
        fields = ["id"]


class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        exclude = ["created_at", "updated_at"]


class CreatorRoyaltyDistributionSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(decimal_places=8, max_digits=15)
    id = serializers.UUIDField(required=False)

    class Meta:
        model = CreatorRoyaltyDistribution
        exclude = ["created_at", "updated_at"]


class IncomeDistributionSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(decimal_places=8, max_digits=15)
    id = serializers.UUIDField(required=False)

    class Meta:
        model = IncomeDistribution
        exclude = ["created_at", "updated_at"]


# TODO: Нужно ? (закомментировал 2.05.2023)
# class NotIdCreatorRoyaltyDistributionSerializer(serializers.ModelSerializer):
#     id = serializers.UUIDField(read_only=True)
#     percent = serializers.DecimalField(
#         decimal_places=8,
#         max_digits=15,
#         required=True,
#     )
#
#     class Meta:
#         model = CreatorRoyaltyDistribution
#         exclude = ["created_at", "updated_at"]
#
#
# class NotIdIncomeDistributionSerializer(serializers.ModelSerializer):
#     id = serializers.UUIDField(read_only=True)
#     percent = serializers.DecimalField(
#         decimal_places=8,
#         max_digits=15,
#         required=True,
#     )
#
#     class Meta:
#         model = IncomeDistribution
#         exclude = ["created_at", "updated_at"]
