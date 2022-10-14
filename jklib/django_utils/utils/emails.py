"""Utility functions for email management in django."""

# Built-in
from threading import Thread
from typing import Any, Dict, List, Optional

# Django
from django.conf import settings
from django.core.mail import EmailMessage

# Local
from .templates import render_template


class Email:
    def __init__(
        self,
        subject: str,
        template_path: str,
    ) -> None:
        self.subject = subject
        self.template_path = template_path

    def send(
        self,
        context: Dict[str, Any],
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
            subject=self.subject,
            body=render_template(self.template_path, context),
            bcc=bcc,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        )
        email.content_subtype = "html"
        email.send()

    def send_async(
        self,
        context: Dict[str, Any],
        bcc: List[str],
    ) -> None:
        thread = Thread(target=self.send, args=(context, bcc))
        thread.start()
