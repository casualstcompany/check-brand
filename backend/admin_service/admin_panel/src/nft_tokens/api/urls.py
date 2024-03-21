from django.urls import include, path

urlpatterns = [
    path("v1/", include("nft_tokens.api.v1.urls")),
]
