# coding: utf-8
"""
Contains useful functions used specifically for this app
Functions:
    get_config: Tries to get the data from django settings, or returns the default value
    render_template: Renders an HTML page using a given template and a given context
"""


# Django
from django.conf import settings
from django.template import loader


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_config(key, default=None):
    """
    Tries to get the data from django settings, or returns the default value
    Args:
        key (str): The data we are looking for in the settings
        default (*): The default value if the key is not found
    Returns:
        (*) The value found in the settings or the default value
    """
    return getattr(settings, key, default)


def render_template(template_path, context):
    """
    Renders an HTML page using a given template and a given context
    Args:
        template_path (str): path to the template (app/template_name)
        context (dict): dict to be used as context
    Returns:
        (str) String containing the dynamically-generated HTML
    """
    template = loader.get_template(template_path)
    rendered = template.render(context)
    return rendered
