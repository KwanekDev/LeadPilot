import hashlib
import secrets
from datetime import datetime
from typing import Optional

from app.core.database import SessionLocal
from app.models.client import Client
from app.core.config import settings


def hash_api_key(api_key: str) -> str:
    salt = settings.API_KEY_PEPPER or ""
    return hashlib.sha256(f"{api_key}{salt}".encode("utf-8")).hexdigest()


def create_client(
    name: str,
    company_name: Optional[str] = None,
    email_user: Optional[str] = None,
    email_password: Optional[str] = None,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
    welcome_subject: Optional[str] = None,
    welcome_body: Optional[str] = None,
    followup_1_subject: Optional[str] = None,
    followup_1_body: Optional[str] = None,
    followup_2_subject: Optional[str] = None,
    followup_2_body: Optional[str] = None,
    api_key: Optional[str] = None,
) -> tuple[Client, str]:
    raw_key = api_key or secrets.token_urlsafe(24)
    encrypted_password = None
    if email_password:
        from app.core.security import encrypt_value

        encrypted_password = encrypt_value(email_password)

    client = Client(
        name=name,
        company_name=company_name,
        api_key_hash=hash_api_key(raw_key),
        email_user=email_user,
        email_password_encrypted=encrypted_password,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        welcome_subject=welcome_subject,
        welcome_body=welcome_body,
        followup_1_subject=followup_1_subject,
        followup_1_body=followup_1_body,
        followup_2_subject=followup_2_subject,
        followup_2_body=followup_2_body,
        enabled=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    with SessionLocal() as session:
        session.add(client)
        session.commit()
        session.refresh(client)
    return client, raw_key


def get_client_by_api_key(api_key: str) -> Optional[Client]:
    hashed = hash_api_key(api_key)
    with SessionLocal() as session:
        return session.query(Client).filter(Client.api_key_hash == hashed).one_or_none()


def get_client_by_id(client_id: int) -> Optional[Client]:
    with SessionLocal() as session:
        return session.query(Client).filter(Client.id == client_id).one_or_none()


def update_client(client_id: int, updates: dict) -> Optional[Client]:
    with SessionLocal() as session:
        client = session.query(Client).filter(Client.id == client_id).one_or_none()
        if not client:
            return None
        for key, value in updates.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)
        client.updated_at = datetime.utcnow()
        session.add(client)
        session.commit()
        session.refresh(client)
        return client
