from django.apps import AppConfig


class NftTokensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nft_tokens"

    def ready(self):
        import nft_tokens.signals
