import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = "s#xonnt5@#t*ci+p%&f*z*$0&@00t7=s12m@-nhywoekav&g2d"

DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS = [i for i in os.environ.get("ALLOWED_HOSTS").split()]
ALLOWED_HOSTS = '*','*'
# CSRF_TRUSTED_ORIGINS = [
#     i for i in os.environ.get("CSRF_TRUSTED_ORIGINS").split()
# ]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]

DOMAIN = os.environ.get("DOMAIN", "checkbrand.com")
HTTP_PROTOCOL = os.environ.get("HTTP_PROTOCOL", "https")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "django_s3_storage",
    "import_export",
    "nft_tokens",
    # "auth_by_grpc",
    # "grps_clients.ugc",
    # "grps_clients.notification",
    "short",
    "django_socio_grpc",
    # "corsheaders",
    "social_opportunities",
    "billing",
    "tools",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": os.environ.get("DB_NAME"),
    #     "USER": os.environ.get("DB_USER"),
    #     "PASSWORD": os.environ.get("DB_PASSWORD"),
    #     "HOST": os.environ.get("DB_HOST"),
    #     "PORT": os.environ.get("DB_PORT", "5432"),
    #     "OPTIONS": {"options": "-c search_path=public,content"},
    # }
    
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "staticfiles"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

URL_BASE_PATH = "admin_service/"
URL_SITE_HEADER = "Checkbrand"
URL_SITE_TITLE = "Checkbrand"
URL_SITE_TITLE_ADMIN = "Панель администратора"

REST_FRAMEWORK = {
    # TODO потом необходимо убрать настройки стандартной авторизации
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    # "DEFAULT_AUTHENTICATION_CLASSES": [
    #     "auth_by_grpc.authentication.JWTGRPCUserAuthentication",
    # ],
}

# TODO потом необходимо убрать настройки стандартной авторизации
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    }
}

APPEND_SLASH = False


AUTH_BY_GRPC = {
    "HOST_GRPC": os.environ.get("AUTH_GRPC_HOST", "localhost"),
    "PORT_GRPC": os.environ.get("AUTH_GRPC_PORT", "50055"),
}


UGC_CLIENT_GRPC = {
    "HOST_GRPC": os.environ.get("UGC_GRPC_HOST", "localhost"),
    "PORT_GRPC": os.environ.get("UGC_GRPC_PORT", "50056"),
}


NOTIFICATION_CLIENT_GRPC = {
    "HOST_GRPC": os.environ.get("NOTIFICATION_GRPC_HOST", "localhost"),
    "PORT_GRPC": os.environ.get("NOTIFICATION_GRPC_PORT", "50053"),
}

DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
AWS_S3_ADDRESSING_STYLE = "auto"
AWS_S3_BUCKET_AUTH = False
AWS_S3_MAX_AGE_SECONDS = None
AWS_S3_PRE_SIGNED_EXPIRES_IN = 600

# TODO добавить сайт убрать лишнее
# CORS_ALLOWED_ORIGINS = [i for i in os.environ.get("CORS_ALLOWED_ORIGINS").split()]

HOST_REDIS = str(os.environ.get("REDIS_HOST"))
REDIS_PORT = str(os.environ.get("REDIS_PORT"))
REDIS_PASSWORD = str(os.environ.get("REDIS_PASSWORD"))

CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{HOST_REDIS}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = (
    f"redis://:{REDIS_PASSWORD}@{HOST_REDIS}:{REDIS_PORT}/0"
)

GRPC_FRAMEWORK = {
    "ROOT_HANDLERS_HOOK": "nft_tokens.handlers.grpc_handlers",
}

BILLING = {
    "TINKOFF_TERMINAL_KEY": os.environ.get("TINKOFF_TERMINAL_KEY"),
    "TINKOFF_PASSWORD": os.environ.get("TINKOFF_PASSWORD"),
    "TINKOFF_LIFETIME_LINK_MUNUTES": os.environ.get(
        "TINKOFF_LIFETIME_LINK_MUNUTES"
    ),
    "TINKOFF_NOTIFICATION_URL": os.environ.get("TINKOFF_NOTIFICATION_URL"),
}

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", 0)),
    profiles_sample_rate=float(
        os.environ.get("SENTRY_PROFILES_SAMPLE_RATE", 0)
    ),
)
