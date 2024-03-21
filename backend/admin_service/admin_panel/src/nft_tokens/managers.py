from django.db import models


class HideManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hide=False)
