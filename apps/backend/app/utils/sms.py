"""
SMS utilities using Twilio
"""

from typing import Optional

from twilio.rest import Client

from app.core.config import settings


def send_sms(to_phone: str, message: str) -> bool:
    """
    Send SMS using Twilio
    """
    if not settings.ENABLE_SMS:
        print("SMS disabled, skipping SMS send")
        return False

    if not all([
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_PHONE_NUMBER
    ]):
        print("Twilio configuration incomplete, skipping SMS send")
        return False

    try:
        # Create Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone
        )

        print(f"SMS sent successfully to {to_phone}, SID: {message.sid}")
        return True

    except Exception as e:
        print(f"Failed to send SMS to {to_phone}: {str(e)}")
        return False