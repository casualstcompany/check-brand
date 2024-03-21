from django_socio_grpc import proto_serializers
from rest_framework import serializers

import nft_tokens.grpc.nft_tokens_pb2 as nft_tokens_pb2
from nft_tokens.models import Token


class TokenProtoSerializer(proto_serializers.ModelProtoSerializer):
    collection = serializers.CharField()

    class Meta:
        model = Token
        proto_class = nft_tokens_pb2.TokenResponse
        proto_class_list = nft_tokens_pb2.TokenListResponse
        fields = [
            "id",
            "status_price",
            "price",
            "status",
            "mint",
            "collection",
            "name",
            "file_1",
        ]

    def to_proto_message(self):
        pass
