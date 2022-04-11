"""Utility functions for email management in django"""

# Built-in
from threading import Thread
from typing import List, Optional, Union

# Django
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage


def extract_email_addresses(emails: Union[List[str], str], sep=",") -> List[str]:
    """Transforms a string of multiple email adresses (separated by commas) into a list"""
    if type(emails) == str:
        emails = emails.split(sep)
    emails = list(map(lambda x: x.strip(), emails))
    return emails


def get_css_content(relative_path: str) -> str:
    """Gets and returns the content of a css file. Avoid using " or ' in your file."""
    css_file = finders.find(relative_path)
    with open(css_file, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def send_html_email(
    subject: str,
    body: str,
    sep: str = ",",
    to: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    sender: Optional[str] = None,
) -> None:
    """Sends an HTML email with the given arguments"""
    to = extract_email_addresses(to, sep)
    cc = extract_email_addresses(cc, sep)
    email = EmailMessage(subject=subject, body=body, to=to, cc=cc, from_email=sender,)
    email.content_subtype = "html"
    email.send()


def send_html_email_async(
    subject: str,
    body: str,
    sep: str = ",",
    to: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    sender: Optional[str] = None,
) -> None:
    """Similar to 'send_html_email', but uses a Thread instance to send it asynchronously"""
    thread = Thread(target=send_html_email, args=(subject, body, sep, to, cc, sender))
    thread.start()
