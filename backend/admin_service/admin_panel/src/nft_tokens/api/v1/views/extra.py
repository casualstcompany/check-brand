from rest_framework import serializers

from auth_by_grpc.permission import AdminOrUserGetGRPCPermission
from nft_tokens import filters, utils
from nft_tokens.api.v1.views import base
from nft_tokens.constants import msg
from nft_tokens.models import (
    Blockchain,
    CurrencyToken,
    LevelsStats,
    Properties,
)
from nft_tokens.serializers import (
    BlockchainSerializer,
    CurrencyTokenSerializer,
    LevelsStatsSerializer,
    PropertiesSerializer,
)


class BlockchainViewSet(base.CustomModelViewSet):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer
    permission_classes = [AdminOrUserGetGRPCPermission]


class CurrencyTokenViewSet(base.CustomModelViewSet):
    filter_backends = (filters.FilterByBlockchainBackend,)
    serializer_class = CurrencyTokenSerializer
    permission_classes = [AdminOrUserGetGRPCPermission]

    def get_queryset(self):
        params = {}

        blockchain_id = self.request.query_params.get("blockchain_id")

        if blockchain_id is not None:
            if not utils.validate_uuid4(blockchain_id):
                raise serializers.ValidationError(
                    {"blockchain_id": msg.blockchain_not_exist}
                )
            try:
                blockchain = Blockchain.objects.get(id=blockchain_id)
            except Blockchain.DoesNotExist:
                raise serializers.ValidationError(
                    {"blockchain_id": msg.blockchain_not_exist}
                )
            utils.set_if_value(params, "blockchain", blockchain)

        queryset = CurrencyToken.objects.filter(**params)

        return queryset


class LevelsStatsViewSet(base.CustomModelViewSet):
    queryset = LevelsStats.objects.all()
    serializer_class = LevelsStatsSerializer
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут


class PropertiesViewSet(base.CustomModelViewSet):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer
    permission_classes = [AdminOrUserGetGRPCPermission]  # TODO: тут
