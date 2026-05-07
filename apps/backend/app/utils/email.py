"""
Email utilities
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    smtp_username: Optional[str] = None,
    smtp_password: Optional[str] = None,
    smtp_tls: Optional[bool] = None,
) -> bool:
    """
    Send email using SMTP with optional tenant-specific settings.
    """
    server_host = smtp_server or settings.SMTP_SERVER
    server_port = smtp_port or settings.SMTP_PORT
    username = smtp_username or settings.SMTP_USERNAME
    password = smtp_password or settings.SMTP_PASSWORD
    tls_enabled = smtp_tls if smtp_tls is not None else settings.SMTP_TLS
    sender = from_email or smtp_username or settings.SMTP_USERNAME

    if not all([server_host, server_port, username, password, sender]):
        print("Email configuration incomplete, skipping email send")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(server_host, server_port)
        if tls_enabled:
            server.starttls()
        server.login(username, password)

        text = msg.as_string()
        server.sendmail(sender, to_email, text)
        server.quit()

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False