"""
Contains useful functions for templating in django
Functions:
    render_template: Renders an HTML page using a given template and a given context
"""


# Django
from django.template import loader


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
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
