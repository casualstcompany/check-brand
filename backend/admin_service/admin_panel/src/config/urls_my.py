from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


# class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
#     def get_schema(self, request=None, public=False):
#         schema = super().get_schema(request, public)
#         schema.schemes = ["http", "https"]
#         return schema



# schema_view = get_schema_view(
#     openapi.Info(
#         title=f"API Admin Panel{settings.URL_SITE_TITLE}",
#         default_version="v1",
#         description=(
#             "На данном этапе набор API предназначен для создания, чтения,"
#             " редактирования и скрытия контента, в следущих версиях API вывода"
#             " контента будут перенесены в отдельный микросервис. Поэтому совет"
#             " предусмотреть это сейчас. Перенесены мудут все Get запросы с"
#             " которыми взаимодействует обычный пользователь"
#         ),
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="mwtech@mail.ru"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],  # TODO: Потом убрать
#     generator_class=BothHttpAndHttpsSchemaGenerator,
# )

# urlpatterns_base = [
    
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("nft_tokens.api.urls")),
    path("api/", include("social_opportunities.api.urls")),
    path("api/", include("billing.api.urls")),
    path('api/shema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# urlpatterns_docs = [
#     # TODO Потом убрать
#     path(
#         "swagger(?P<format>\.json|\.yaml)",
#         schema_view.without_ui(cache_timeout=0),
#         name="schema-json",
#     ),
#     path(
#         "swagger/",
#         schema_view.with_ui("swagger", cache_timeout=0),
#         name="schema-swagger-ui",
#     ),
#     path(
#         "redoc/",
#         schema_view.with_ui("redoc", cache_timeout=0),
#         name="schema-redoc",
#     ),
# ]

# urlpatterns = [
#     path(settings.URL_BASE_PATH, include(urlpatterns_base)),
#     path(settings.URL_BASE_PATH, include(urlpatterns_docs)),
# ]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

admin.site.site_header = settings.URL_SITE_HEADER
admin.site.index_title = settings.URL_SITE_TITLE_ADMIN
admin.site.site_title = settings.URL_SITE_TITLE
