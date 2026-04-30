import base64
import os

from cryptography.fernet import Fernet

from app.core.config import settings


def _get_fernet_key() -> bytes:
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("ENCRYPTION_KEY is required for secure password storage.")
    try:
        return base64.urlsafe_b64decode(key)
    except Exception as error:
        raise ValueError("ENCRYPTION_KEY must be a valid base64 urlsafe-encoded key.") from error


def _get_cipher() -> Fernet:
    raw_key = _get_fernet_key()
    if len(raw_key) != 32:
        raise ValueError("ENCRYPTION_KEY must decode to 32 bytes.")
    return Fernet(base64.urlsafe_b64encode(raw_key))


def encrypt_value(value: str) -> str:
    cipher = _get_cipher()
    return cipher.encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    cipher = _get_cipher()
    return cipher.decrypt(value.encode("utf-8")).decode("utf-8")
