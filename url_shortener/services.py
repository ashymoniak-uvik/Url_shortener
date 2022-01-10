import json
import random
import string
from json import JSONDecodeError

import requests as requests
import validators as validators
from django.forms import Form
from django.http import HttpRequest

from url_shortener.models import ShortenedURL


def get_context(form: Form, request: HttpRequest) -> dict:
    """
    This function is responsible for retrieving the context dict which we
    have been preparing in the _prepare_context_for_response() funtion.
    Also, inside this function we validate the provided url.
    """
    error, url = _get_url_from_body(form.cleaned_data["request_body"])
    slug = _create_short_url()

    if url:
        url_obj, error, shortened_url = _validate_shorten_url(request, url, slug)
        if error:
            context = _prepare_context_for_response(form, request, error)
        else:
            context = _prepare_context_for_response(
                form, request, url_obj, shortened_url
            )
    else:
        context = _prepare_context_for_response(form, request, error)
    return context


def _prepare_context_for_response(form: Form, request: HttpRequest,
                                  url_obj: ShortenedURL,
                                  shortened_url: str = None) -> dict:
    """
    This function is responsible for context dict for the response
    """

    original_site_data = None
    if isinstance(url_obj, ShortenedURL):
        body = {"status_code": 201, "response_body": {}}
        if shortened_url:
            body["response_body"]["original_url"] = url_obj.long_url

            original_site_data = requests.get(url_obj.long_url, {}).text
        else:
            body["response_body"] = {
                "shortened_url": f"{request.scheme}://{request.get_host()}"
                f"/{url_obj.short_url}",
                "shortened_urls": f"{url_obj.counter}",
            }

    else:
        body = {
            "status_code": 403,
            "response_body": {
                "error": f"{url_obj}",
            },
        }
    return {
        "form": form,
        "request_body": json.dumps(body, indent=4),
        "original_site_data": original_site_data,
    }


def _create_short_url() -> str:
    """
    This function is responsible for creating slug
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


def _get_url_from_body(request_body: str) -> tuple:
    """
    This function is used to retrieve valid URL from the request body

    Returns tuple with the error and url. The error will be None in case no
    errors happen and the URL will contain the validated URL. In case any
    error appears we will return the error message and None instead of the URL.
    """

    error_message = {
        "keyword_error": "'url' keyword is missed",
        "incorrect_body": "Incorrect body is provided. Please use the "
        "following structure for request: {'url': 'original_url'}",
        "incorrect_url": "Incorrect 'url' is provided",
    }
    try:
        body = json.loads(request_body)
        if isinstance(body, dict):
            if "url" in body:
                if validators.url(body["url"]):
                    return None, body["url"]
                else:
                    return error_message["incorrect_url"], None
            return error_message["keyword_error"], None
        return error_message["incorrect_body"], None
    except (TypeError, JSONDecodeError):
        return error_message["incorrect_body"], None


def _validate_shorten_url(request, url: str, slug: str) -> tuple:
    """
    This function is responsible for validation shorten url.
    If url is already shortened and user provide the short version of URL we
    will return a tuple with shortened object, None as error and short url
    If user provided URL for external resource we will create or update the
    shortened url object and return shortened object, None as error,
    and None as short url
    """
    if f"{request.scheme}://{request.get_host()}" in url:
        try:
            url_obj = ShortenedURL.objects.get(short_url=url.split("/")[-1])
            return url_obj, None, url_obj.short_url
        except ShortenedURL.DoesNotExist:
            return None, "Incorrect 'url' is provided", None

    else:
        return _update_or_create_shorten_url(slug, url)


def _update_or_create_shorten_url(slug: str, url: str) -> tuple:
    """
    This function is responsible for creation or updating the shortened url
    object
    """
    url_obj, created = ShortenedURL.objects.get_or_create(long_url=url)
    if created:
        url_obj.short_url = slug
    url_obj.counter += 1
    url_obj.save()
    return url_obj, None, None
