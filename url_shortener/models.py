from django.db import models


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    long_url = models.URLField(unique=True)
    short_url = models.URLField(blank=True, null=True)
    counter = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Shortened URLs"
        verbose_name = "Shortened URL"

    def __str__(self):
        return str(self.long_url)


class IpAddress(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    shorten_url = models.ForeignKey(
        ShortenedURL, on_delete=models.CASCADE, related_name="ip_address"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "IP Addresses"
        verbose_name = "IP Address"
