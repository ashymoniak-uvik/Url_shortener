from django.contrib import admin

from url_shortener.models import ShortenedURL, IpAddress

admin.site.register(ShortenedURL)
admin.site.register(IpAddress)
