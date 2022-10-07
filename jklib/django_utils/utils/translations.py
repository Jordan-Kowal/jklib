"""Scripts for handling translations within django."""

# Built-in
import os
from typing import List


def update_translations(languages: List[str]) -> None:
    """Updates the translations for the given languages."""
    # Get the directory with manage.py
    project_root = os.getcwd()
    project_name = project_root.split("\\")[-1]
    target_dir = os.path.join(project_root, project_name)
    os.chdir(target_dir)
    # Execute our code
    for language in languages:
        os.system(f"django-admin makemessages -l {language} -e py,html")
    # Go back to normal
    os.chdir(project_root)
