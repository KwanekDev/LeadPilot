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
    from_email: Optional[str] = None
) -> bool:
    """
    Send email using SMTP
    """
    if not all([
        settings.SMTP_SERVER,
        settings.SMTP_PORT,
        settings.SMTP_USERNAME,
        settings.SMTP_PASSWORD
    ]):
        print("Email configuration incomplete, skipping email send")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email or settings.SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(body, 'html'))

        # Create SMTP connection
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)

        if settings.SMTP_TLS:
            server.starttls()

        # Login
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

        # Send email
        text = msg.as_string()
        server.sendmail(settings.SMTP_USERNAME, to_email, text)

        # Close connection
        server.quit()

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False