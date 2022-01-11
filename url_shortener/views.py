import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from url_shortener.forms import URLForm
from url_shortener.services import get_context


def shorten_url(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = URLForm(request.POST)

        if form.is_valid():
            context = get_context(form, request)
            return render(request, "index.html", context)
    else:
        form = URLForm()

    context = {"form": form, "request_body": json.dumps({"url": ""}, indent=4)}

    return render(request, "index.html", context)
