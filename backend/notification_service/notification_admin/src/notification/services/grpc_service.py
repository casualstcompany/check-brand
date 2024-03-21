from django_socio_grpc import generics

from notification.models import TemplateMail
from notification.serializers import TemplateMailProtoSerializer


class TemplateMailService(generics.AsyncReadOnlyModelService):
    queryset = TemplateMail.objects.all()
    serializer_class = TemplateMailProtoSerializer
    lookup_request_field = "content_type"
