import os
from pathlib import Path
import base64

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://leadpilot:leadpilot@db:5432/leadpilot")
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "CHANGE_ME_ADMIN")
    API_KEY_PEPPER: str = os.getenv("API_KEY_PEPPER", "CHANGE_ME_PEPPER")
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", base64.urlsafe_b64encode(os.urandom(32)).decode())
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_PASS: str = os.getenv("GMAIL_PASS", "")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    GOOGLE_CREDENTIALS_PATH: Path = Path("google_creds.json")
    DEFAULT_SHEET_NAME: str = "Leads"
    GOOGLE_SHEETS_NAME: str = "LeadPilot_Leads"


settings = Settings()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key == settings.ADMIN_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API key.",
    )