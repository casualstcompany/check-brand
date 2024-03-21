from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "AUTH_BY_GRPC", None)

DEFAULTS = {
    "PORT_GRPC": "50055",
    "HOST_GRPC": "localhost",
}

grpc_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_grpc_settings(*args, **kwargs):
    global grpc_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "AUTH_BY_GRPC":
        grpc_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_grpc_settings)
