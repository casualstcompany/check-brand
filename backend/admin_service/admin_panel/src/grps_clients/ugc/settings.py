from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "UGC_CLIENT_GRPC", None)

DEFAULTS = {
    "PORT_GRPC": "50056",
    "HOST_GRPC": "localhost",
}

ugc_grpc_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_grpc_settings(*args, **kwargs):
    global ugc_grpc_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "UGC_CLIENT_GRPC":
        ugc_grpc_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_grpc_settings)
