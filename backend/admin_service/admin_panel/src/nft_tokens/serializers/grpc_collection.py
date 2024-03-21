from django_socio_grpc import proto_serializers
from rest_framework import serializers

import nft_tokens.grpc.nft_tokens_pb2 as nft_tokens_pb2
from nft_tokens.models import Collection


class CollectionProtoSerializer(proto_serializers.ModelProtoSerializer):
    account = serializers.CharField()

    class Meta:
        model = Collection
        proto_class = nft_tokens_pb2.CollectionResponse
        proto_class_list = nft_tokens_pb2.CollectionListResponse
        fields = [
            "id",
            "logo",
            "name",
            "status",
            "account",
        ]

    def to_proto_message(self):
        pass
