"""Functions for managing templates in django"""

# Django
from django.template import loader


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def render_template(template_path, context):
    """
    Renders an HTML page using a given template and a given context
    :param str template_path: Path to the template (app/template_name)
    :param dict context: The context values
    :return: The dynamically-generated HTML
    :rtype: str
    """
    template = loader.get_template(template_path)
    rendered = template.render(context)
    return rendered
