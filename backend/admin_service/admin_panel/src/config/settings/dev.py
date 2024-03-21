from .base import *

DEBUG = True

LOGGING = {
    "disable_existing_loggers": False,
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db": {"level": "DEBUG"},
    },
}
