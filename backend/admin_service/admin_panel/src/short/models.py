from django.db import models


class ShortURL(models.Model):
    collection_name = models.CharField(max_length=255)
    token_name = models.CharField(max_length=255)
    full_url = models.URLField(unique=False)
    url_hash = models.SlugField(unique=True)
    clicks = models.IntegerField(default=0)
    generate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url_hash

    class Meta:
        verbose_name = "Short url"
        verbose_name_plural = "Short urls"
        db_table = 'content"."short_url'
