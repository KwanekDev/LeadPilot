import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, content: str) -> bool:
    """Send an email via Gmail SMTP with error handling and logging."""
    try:
        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_PASS")

        if not gmail_user or not gmail_pass:
            logger.error("Missing GMAIL_USER or GMAIL_PASS environment variables.")
            return False

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = gmail_user
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {e}. Check GMAIL_USER and GMAIL_PASS.")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email to {to_email}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email to {to_email}: {e}")
        return False