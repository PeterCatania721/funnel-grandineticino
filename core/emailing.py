"""Invio email condiviso tra sito KESI e funnel Grandineticino."""
import logging
from typing import Iterable, Sequence

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def lead_recipient_email() -> str:
    """Destinatario unico per lead e preventivi (default: company.email)."""
    return settings.LEAD_RECIPIENT_EMAIL


def send_lead_notification(
    *,
    subject: str,
    body: str,
    reply_to: str | Sequence[str],
    attachments: Iterable | None = None,
) -> None:
    """Invia notifica a info@kesi.biz con allegati opzionali."""
    reply_list = [reply_to] if isinstance(reply_to, str) else list(reply_to)
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[lead_recipient_email()],
        reply_to=reply_list,
    )
    _attach_all(msg, attachments or ())
    msg.send()


def _attach_all(msg: EmailMessage, attachments: Iterable) -> None:
    for attachment in attachments:
        if hasattr(attachment, "file"):
            attachment.file.open("rb")
            try:
                msg.attach(
                    attachment.original_name or attachment.file.name,
                    attachment.file.read(),
                    "application/octet-stream",
                )
            finally:
                attachment.file.close()
        elif hasattr(attachment, "read"):
            content = attachment.read()
            if hasattr(attachment, "seek"):
                attachment.seek(0)
            msg.attach(
                attachment.name,
                content,
                getattr(attachment, "content_type", "application/octet-stream"),
            )
        else:
            name, content, mimetype = attachment
            msg.attach(name, content, mimetype)
