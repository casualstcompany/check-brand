from django.conf import settings
from django.core.signals import setting_changed

APP_BILLING = "BILLING"

DEFAULTS = {
    "TINKOFF_TERMINAL_KEY": "string",
    "TINKOFF_PASSWORD": "string",
    "TINKOFF_LIFETIME_LINK_MUNUTES": 1440,
    "TINKOFF_NOTIFICATION_URL": "string",
}


class BillingSettings:
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, APP_BILLING, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


billing_settings = BillingSettings(None, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == APP_BILLING:
        billing_settings.reload()


setting_changed.connect(reload_api_settings)
