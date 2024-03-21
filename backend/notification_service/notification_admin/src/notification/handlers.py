from django_socio_grpc.utils.servicer_register import AppHandlerRegistry

from notification.services import TemplateMailService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("notification", server)
    app_registry.register(TemplateMailService)
