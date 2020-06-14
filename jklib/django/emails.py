"""
Contains useful functions used specifically for this app
Functions:
    extract_email_addresses: Returns a list of emails from either a string or a list
    get_css_content: Returns the content of a css file (AVOID using " or ' in the file)
    send_html_email: Sends an HTML email with the given arguments
"""


# Django
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def extract_email_addresses(emails):
    """
    Transforms a string of multiple email adresses (separated by commas) into a list
    Args:
        emails (string): Long string of emails separated with commas
    Returns:
        (list) A list of email addresses
    """
    if type(emails) == str:
        emails = emails.split(",")
        emails = list(map(lambda x: x.strip(), emails))
    return emails


def get_css_content(relative_path):
    """
    Gets and returns the content of a css file (AVOID using " or ' in the file)
    Args:
        relative_path (str): Relative path to the CSS file (the path you'd use in a django template with {% static %})
    Returns:
        (str) The content of the CSS file
    """
    css_file = finders.find(relative_path)
    with open(css_file, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def send_html_email(subject, body, to=None, cc=None, sender=None):
    """
    Sends an HTML email with the given arguments
    Args:
        subject (str): Subject of the email
        body (str): Body/Content of the email
        to ([str, list], optional): List or comma-separated string of emails. Defaults to None.
        cc ([str, list], optional): List or comma-separated string of emails. Defaults to None.
        sender (str, optional): The sender. Defaults to Django configuration.
    """
    to = extract_email_addresses(to)
    cc = extract_email_addresses(cc)
    email = EmailMessage(subject=subject, body=body, to=to, cc=cc, from_email=sender,)
    email.content_subtype = "html"
    email.send()
