import hashlib
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings
from app.services.client_service import get_client_by_api_key
from app.core.database import SessionLocal
from app.models.admin import AdminUser

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
admin_token_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)

def hash_api_key(api_key: str) -> str:
    salt = settings.API_KEY_PEPPER or ""
    return hashlib.sha256(f"{api_key}{salt}".encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    salt = settings.API_KEY_PEPPER or ""
    return hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()

def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key.",
        )
    return api_key

def get_current_client(api_key: str = Depends(verify_api_key)):
    client = get_client_by_api_key(api_key)
    if not client or not client.enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )
    return client

def get_admin(
    api_key: Optional[str] = Security(api_key_header),
    admin_token: Optional[str] = Security(admin_token_header)
) -> str:
    if api_key == settings.ADMIN_API_KEY:
        return api_key
    
    if admin_token:
        with SessionLocal() as session:
            admin = session.query(AdminUser).filter(AdminUser.session_token == admin_token).first()
            if admin:
                return admin.email

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid admin credentials.",
    )