from .views import shorten_url
from django.urls import path

urlpatterns = [
    path('shorten-the-url/', shorten_url, name='shorten_url'),
]