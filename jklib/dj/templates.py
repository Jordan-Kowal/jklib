# Built-in
from typing import Dict

# Django
from django.template import loader


def render_template(template_path: str, context: Dict) -> str:
    """Renders a template with the given context."""
    template = loader.get_template(template_path)
    rendered = template.render(context)
    return rendered
