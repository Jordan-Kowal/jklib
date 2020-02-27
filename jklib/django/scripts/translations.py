# coding: utf-8
"""
Description:
    Scripts for handling translations within Django
Functions:
    update_translations: Updates the translations for the given languages
"""


# Built-in
import os


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def update_translations(languages):
    """
    Description:
        Updates the translations for the given languages
        The languages must be in the shape of their relative folders: fr_FR, en_US, etc.
    Args:
        languages (list): List of strings that represent the languages
    """
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
