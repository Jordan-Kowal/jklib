"""Decorators for django"""


# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def render_to(template):
    """
    Decorator that renders a django view to a specific template
    Functions using the decorator must simply return the context dict
    :param template: The django path to our template
    :return: Our rendered template in a HttpResponse
    :rtype: HttpResponse
    """

    def renderer(function):
        def wrapper(request, *args, **kwargs):
            response = function(request, *args, **kwargs)
            if isinstance(response, (HttpResponse, HttpResponseRedirect)):
                return response
            return render(request, template_name=template, context=response)

        return wrapper

    return renderer
