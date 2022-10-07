"""Decorators for django."""


# Built-in
from typing import Any, Callable

# Django
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def render_to(template: str) -> Callable:
    """Decorator that renders a django view to a specific template Functions
    using the decorator must simply return the context dict."""

    def renderer(function: Callable) -> Callable:
        def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            response: HttpResponse = function(request, *args, **kwargs)
            if isinstance(response, (HttpResponse, HttpResponseRedirect)):
                return response
            return render(request, template_name=template, context=response)

        return wrapper

    return renderer
