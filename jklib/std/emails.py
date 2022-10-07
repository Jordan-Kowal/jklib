"""Utility functions to deal with emails."""


# Built-in
import os
import smtplib
from email.message import EmailMessage
from typing import Sequence, Tuple, Type, Union


def attach_files(message: EmailMessage, path: str) -> EmailMessage:
    """Attaches our files to our EmailMessage instance (only if they are PDF or
    images)"""
    files = [os.path.join(path, f) for f in os.listdir(path)]
    for file in files:
        params = {}
        with open(file, "rb") as f:
            file_name = os.path.basename(f.name)
            file_type = os.path.splitext(file_name)[1][1:]
            file_data = f.read()
        # We attach the file based on its type
        if file_type == "pdf":
            params["maintype"] = "application"
            params["subtype"] = "octet_stream"
        elif file_type in {"jpg", "jpeg", "png", "gif"}:
            params["maintype"] = "image"
            params["subtype"] = file_type
        else:
            continue
        params["filename"] = file_name
        message.add_attachment(file_data, **params)  # type: ignore
    return message


def choose_smtp_class(
    port: int,
) -> Tuple[Union[Type[smtplib.SMTP], Type[smtplib.SMTP_SSL]], bool]:
    """Chooses the right SMTP class to connect to the server based on the given
    port."""
    smtp: Union[Type[smtplib.SMTP], Type[smtplib.SMTP_SSL]]
    if port == 465:
        smtp = smtplib.SMTP_SSL
        ssl = True
    else:
        smtp = smtplib.SMTP
        ssl = False
    return smtp, ssl


def connect_without_ssl(server: smtplib.SMTP) -> None:
    """Tries to connect to the smtp server without SSL, using TLS or not
    security protocol at all."""
    try:
        server.starttls()
    except smtplib.SMTPException():  # type: ignore
        pass
    finally:
        server.ehlo()


def create_message() -> EmailMessage:
    """Creates and returns an EmailMessage instance."""
    message = EmailMessage()
    message["Subject"] = ""
    message["From"] = ""
    # BCC must not be added to the headers
    addresses: Sequence[str]
    for text, addresses in zip(["To", "Cc", "Bcc"], [[], [], []]):
        if addresses:
            message[text] = ", ".join(addresses)
    # message.set_content("Sent from python")
    html_content = ""
    message.add_alternative(html_content, subtype="html")
    return message


def email_auth(server: smtplib.SMTP, ssl: bool) -> bool:
    """Authenticates with the server, using either SSL, TLS, or no security
    protocol."""
    if not ssl:
        connect_without_ssl(server)
    try:
        server.login("login", "key")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentification failed:", e)
        print("Exiting program...")
        return False
    else:
        print("Authentification successful.")
        return True


def get_template(path: str) -> str:
    """Gets the HTML template and replaces patterns in a "template-like"
    manner."""
    with open(path, "r", encoding="utf-8") as f:
        f_content = f.read()
    # Getting the store list and placing it in the template
    for element, pattern in zip(["a", "b"], ["{{pattern1}}", "{{pattern2}}"]):
        f_content = f_content.replace(pattern, element)
    return f_content
