"""Functions for managing templates in django."""

# Built-in
from typing import Dict

# Django
from django.template import loader


def render_template(template_path: str, context: Dict) -> str:
    """Renders an HTML page using a given template and a given context."""
    template = loader.get_template(template_path)
    rendered = template.render(context)
    return rendered
