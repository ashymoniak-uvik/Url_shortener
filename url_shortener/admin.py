from django.contrib import admin

# Register your models here.
from url_shortener.models import ShortenedURL

admin.site.register(ShortenedURL)
