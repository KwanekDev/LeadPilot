import os
from dotenv import load_dotenv
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Nie masz uprawnień do tego zasobu."
    )