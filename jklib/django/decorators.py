# coding: utf-8
"""
Description:
    This file contains useful decorators for Django
Functions:
    render_to: Decorator that renders a django view to a specific template
"""


# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def render_to(template):
    """
    Description:
        Decorator that renders a django view to a specific template
        Functions using the decorator must simply return the context dict
    Args:
        template (str): The template path
    Returns:
        (HttpResponse) Renders the page with the given template and context
    """

    def renderer(function):
        def wrapper(request, *args, **kwargs):
            response = function(request, *args, **kwargs)
            if isinstance(response, (HttpResponse, HttpResponseRedirect)):
                return response
            return render(request, template_name=template, context=response)

        return wrapper

    return renderer
