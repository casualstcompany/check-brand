from django.urls import include, path

urlpatterns = [
    path("v1/", include("social_opportunities.api.v1.urls")),
]
