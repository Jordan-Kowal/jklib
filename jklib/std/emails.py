# coding: utf8
"""
Functions to easily work with emails and email servers
Functions:
    attach_pdfs: Attaches our files to our EmailMessage instance (only if they are PDF or images)
    choose_smtp_class: Choose the right SMTP class to connect to the server based on the given port
    connect_without_ssl: Tries to connect to the smtp server without SSL, using TLS or not security protocol at all
    create_message: Creates and returns an EmailMessage instance
    email_auth: Authenticates with the server, using either SSL, TLS, or no security protocol
    get_template: Gets the HTML template and replaces patterns in a "template-like" manner
"""


# Built-in
import os
import smtplib
from email.message import EmailMessage


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def attach_files(message, path):
    """
    Attaches our files to our EmailMessage instance (only if they are PDF or images)
    Args:
        message (EmailMessage): Our current EmailMessage instance
        path (str): Path of the folder that contains our files
    Returns:
        (EmailMessage) The updated EmailMessage instance, now with files attached
    """
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
        message.add_attachment(file_data, **params)
    return message


def choose_smtp_class(port):
    """
    Choose the right SMTP class to connect to the server based on the given port
    Args:
        port (int): Port on which to connect
    Returns:
        (tuple) The correct SMTP class and a bool to indicate if we are in SSL
    """
    if port == 465:
        smtp = smtplib.SMTP_SSL
        ssl = True
    else:
        smtp = smtplib.SMTP
        ssl = False
    return smtp, ssl


def connect_without_ssl(server):
    """
    Tries to connect to the smtp server without SSL, using TLS or not security protocol at all
    Args:
        server (SMTP or SMTP_SSL): A type of smtp instance from smtplib
    """
    try:
        server.starttls()
    except smtplib.SMTPException():
        pass
    finally:
        server.ehlo()


def create_message():
    """
    Creates and returns an EmailMessage instance
    This is the email we will send at the end of the process
    Returns:
        (EmailMessage) A ready-to-send EmailMessage with information and attachments
    """
    message = EmailMessage()
    message["Subject"] = ""
    message["From"] = ""
    # BCC must not be added to the headers
    for text, addresses in zip(["To", "Cc", "Bcc"], [[], [], []]):
        if addresses:
            message[text] = ", ".join(addresses)
    # message.set_content("Envoyé depuis Python")
    html_content = ""
    message.add_alternative(html_content, subtype="html")
    message = attach_files(message)
    return message


def email_auth(server, ssl):
    """
    Authenticates with the server, using either SSL, TLS, or no security protocol
    Will return a bool indicating if authentification was successful
    Args:
        server (SMTP or SMTP_SSL): A type of smtp instance from smtplib
        ssl (bool): Indicates whether we can use SSL
    Returns:
        (bool) Indicates whether the authentification was successful
    """
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


def get_template(path):
    """
    Gets the HTML template and replaces patterns in a "template-like" manner
    Returns the updated HTML template
    Args:
        path (str): Path to the initial HTML template/file
    Returns:
        (str) The updated HTML content as string
    """
    with open(path, "r", encoding="utf-8") as f:
        f_content = f.read()
    # Getting the store list and placing it in the template
    for element, pattern in zip(["a", "b"], ["{{pattern1}}", "{{pattern2}}"]):
        f_content = f_content.replace(pattern, element)
    return f_content
