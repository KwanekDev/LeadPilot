import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings
from app.core.security import decrypt_value

logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    content: str,
    smtp_user: Optional[str] = None,
    smtp_password_encrypted: Optional[str] = None,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
) -> bool:
    from_email = smtp_user or settings.GMAIL_USER
    password = None
    if smtp_password_encrypted:
        try:
            password = decrypt_value(smtp_password_encrypted)
        except Exception as error:
            logger.error("Failed to decrypt SMTP password: %s", error)
            return False
    else:
        password = settings.GMAIL_PASS

    if not from_email or not password:
        logger.error("SMTP credentials are not configured.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email
    message.set_content(content)

    smtp_host = smtp_host or settings.SMTP_HOST
    smtp_port = smtp_port or settings.SMTP_PORT

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(from_email, password)
            server.send_message(message)

        logger.info("Email sent to %s using %s", to_email, from_email)
        return True
    except smtplib.SMTPAuthenticationError as error:
        logger.error("SMTP auth failed: %s", error)
        return False
    except smtplib.SMTPException as error:
        logger.error("SMTP error sending email to %s: %s", to_email, error)
        return False
    except Exception as error:
        logger.error("Unexpected error sending email to %s: %s", to_email, error)
        return False
