from django.db import models


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    long_url = models.URLField(unique=True)
    short_url = models.URLField(blank=True, null=True)
    counter = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Shortened URLs'
        verbose_name = 'Shortened URL'
