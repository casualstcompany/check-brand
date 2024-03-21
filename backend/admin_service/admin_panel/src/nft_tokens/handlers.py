from django_socio_grpc.utils.servicer_register import AppHandlerRegistry

from nft_tokens.services.grpc_collection_service import CollectionGrpcService
from nft_tokens.services.grpc_token_service import TokenGrpcService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("nft_tokens", server)
    app_registry.register(CollectionGrpcService)
    app_registry.register(TokenGrpcService)
