from rest_framework import serializers

from nft_tokens.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ["created_at", "updated_at"]


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "name", "number", "url", "banner", "icon"]
        lookup_field = "url"


class HidePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["hide"]
