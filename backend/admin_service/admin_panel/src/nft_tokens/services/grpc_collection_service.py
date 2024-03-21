from django_socio_grpc import generics

from nft_tokens.models import Collection
from nft_tokens.serializers.grpc_collection import CollectionProtoSerializer


class CollectionGrpcService(generics.AsyncReadOnlyModelService):
    queryset = Collection.objects.all()
    serializer_class = CollectionProtoSerializer
