from django_socio_grpc import generics

from nft_tokens.models import Token
from nft_tokens.serializers.grpc_token import TokenProtoSerializer


class TokenGrpcService(generics.AsyncReadOnlyModelService):
    queryset = (
        Token.objects.select_related("collection")
        .only(
            "id",
            "status_price",
            "price",
            "status",
            "mint",
            "collection__id",
            "name",
            "file_2",
        )
        .all()
    )
    serializer_class = TokenProtoSerializer
