from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns_base = [
    path('admin/', admin.site.urls),
    path('notification/', include("notification.urls")),
]


urlpatterns = [
    path(settings.URL_BASE_PATH, include(urlpatterns_base)),
]

admin.site.site_header = settings.URL_SITE_HEADER
admin.site.index_title = settings.URL_SITE_TITLE_ADMIN
admin.site.site_title = settings.URL_SITE_TITLE
