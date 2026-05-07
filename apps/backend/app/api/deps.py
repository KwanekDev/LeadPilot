"""API dependencies"""
from typing import Any, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app import crud, models
from app.core import auth
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token"
)
admin_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/admin-access-token"
)


class AdminPrincipal(BaseModel):
    email: str
    role: str = "admin"


def get_db() -> Generator:
    """Database session dependency"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Any:
    """Get current authenticated regular user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[auth.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        token_scope: str = payload.get("scope")
        if user_id is None or role != "user" or token_scope != "access":
            raise credentials_exception
    except (jwt.JWTError, ValidationError):
        raise credentials_exception

    user = crud.user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Get current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_admin(
    token: str = Depends(admin_oauth2),
) -> AdminPrincipal:
    """Get currently authenticated system admin from token/env."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[auth.ALGORITHM])
        subject = payload.get("sub")
        role = payload.get("role")
        token_scope = payload.get("scope")
    except jwt.JWTError:
        raise credentials_exception

    if role != "admin" or token_scope != "access" or subject != settings.ADMIN_EMAIL:
        raise credentials_exception

    return AdminPrincipal(email=settings.ADMIN_EMAIL)