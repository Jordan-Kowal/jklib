"""Utility functions for email management in django"""


# Django
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def extract_email_addresses(emails, sep=","):
    """
    Transforms a string of multiple email adresses (separated by commas) into a list
    :param str emails: Single string of emails separated by a specific character
    :param str sep: The separator used in the emails parameter. Defaults to ','
    :return: A list of email addresses
    :rtype: list(str)
    """
    if type(emails) == str:
        emails = emails.split(",")
        emails = list(map(lambda x: x.strip(), emails))
    return emails


def get_css_content(relative_path):
    """
    Gets and returns the content of a css file
    Please make your that CSS file do not use " or '
    :param relative_path: Relative path to the CSS file (the same as the one you'd use in {% static %})
    :return: The content of the CSS file
    :rtype: str
    """
    css_file = finders.find(relative_path)
    with open(css_file, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def send_html_email(subject, body, sep=",", to=None, cc=None, sender=None):
    """
    Sends an HTML email with the given arguments
    :param str subject: Subject of the email
    :param str body: Body/content of the email
    :param str sep: The separator used in the emails parameter. Defaults to ','
    :param to: List or character-separated string of emails. Defaults to None.
    :type to: list(str) or str
    :param cc: List or character-separated string of emails. Defaults to None.
    :type cc: list(str) or str
    :param str sender: The sender. Defaults to django configuration.
    """
    to = extract_email_addresses(to)
    cc = extract_email_addresses(cc)
    email = EmailMessage(subject=subject, body=body, to=to, cc=cc, from_email=sender,)
    email.content_subtype = "html"
    email.send()
