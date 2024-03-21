from django_socio_grpc import proto_serializers
from rest_framework import serializers

import notification.grpc.notification_pb2 as notification_pb2
from notification.models import TemplateMail


class TemplateMailProtoSerializer(proto_serializers.ModelProtoSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = TemplateMail
        proto_class = notification_pb2.TemplateMailResponse
        proto_class_list = notification_pb2.TemplateMailListResponse
        fields = ["id", "content_type", "subject", "body_html", "body_text"]

    def to_proto_message(self):
        pass
