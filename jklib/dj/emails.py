# Built-in
from threading import Thread
from typing import Any, Dict, List, Optional

# Django
from django.conf import settings
from django.core.mail import EmailMessage

# Application
from jklib.dj.templates import render_template


class Email:
    def __init__(
        self,
        default_subject: str,
        template_path: str,
    ) -> None:
        self.default_subject = default_subject
        self.template_path = template_path

    def send(
        self,
        context: Dict[str, Any],
        subject: Optional[str] = None,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        from_email: Optional[str] = None,
    ) -> None:
        to = to or []
        cc = cc or []
        bcc = bcc or []
        # Skip if no recipients
        if not to and not cc and not bcc:
            return
        email = EmailMessage(
            subject=subject or self.default_subject,
            body=render_template(self.template_path, context),
            to=to,
            cc=cc,
            bcc=bcc,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        )
        email.content_subtype = "html"
        email.send()

    def send_async(
        self,
        context: Dict[str, Any],
        subject: Optional[str] = None,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        from_email: Optional[str] = None,
    ) -> None:
        thread = Thread(
            target=self.send, args=(context, subject, to, cc, bcc, from_email)
        )
        thread.start()
