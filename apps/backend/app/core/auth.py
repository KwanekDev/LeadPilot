"""
Authentication and Security utilities
"""

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Konfiguracja haszowania haseł (bcrypt dla kompatybilności)
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto", 
    bcrypt__default_rounds=12, 
    bcrypt__ident="2b"
)

ALGORITHM = "HS256"

# --- TOKENY JWT ---

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    role: str = "user",
    token_scope: str = "access",
) -> str:
    """Tworzy token dostępu JWT"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "role": role, "scope": token_scope}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], role: str = "user") -> str:
    """Tworzy token odświeżania JWT"""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "scope": "refresh", "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Union[dict, None]:
    """Weryfikuje token JWT i zwraca identyfikator (sub)"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return payload
    except jwt.JWTError:
        return None

# --- WERYFIKACJA HASEŁ ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Weryfikuje hasło (wspiera SHA256 jako fallback i bcrypt)"""
    # Fallback dla starych haseł/kluczy systemowych
    sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    if hashed_password == sha256_hash:
        return True
    
    # Standardowa weryfikacja bcrypt
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generuje hash bcrypt z hasła"""
    return pwd_context.hash(password)