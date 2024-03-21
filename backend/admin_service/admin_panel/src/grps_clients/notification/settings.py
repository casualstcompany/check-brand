from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "NOTIFICATION_CLIENT_GRPC", None)

DEFAULTS = {
    "PORT_GRPC": "50056",
    "HOST_GRPC": "localhost",
}

notification_grpc_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_grpc_settings(*args, **kwargs):
    global notification_grpc_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "NOTIFICATION_CLIENT_GRPC":
        notification_grpc_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_grpc_settings)
