"""Authentication endpoints."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import auth
from app.core.config import settings
from app.core.logging_config import log_login_attempt

router = APIRouter()
_ADMIN_LOGIN_ATTEMPTS: Dict[str, list[datetime]] = {}
_ADMIN_MAX_ATTEMPTS = 5
_ADMIN_WINDOW_SECONDS = 300


def _prune_attempts(attempts: list[datetime]) -> list[datetime]:
    now = datetime.now(timezone.utc)
    return [
        ts
        for ts in attempts
        if (now - ts).total_seconds() <= _ADMIN_WINDOW_SECONDS
    ]


@router.post("/admin-access-token", response_model=schemas.Token)
def login_admin_access_token(
    *,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Dedicated admin login based on env credentials."""
    ip_address = request.client.host if request.client else "unknown"
    attempts = _prune_attempts(_ADMIN_LOGIN_ATTEMPTS.get(ip_address, []))
    _ADMIN_LOGIN_ATTEMPTS[ip_address] = attempts
    if len(attempts) >= _ADMIN_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed admin login attempts. Try again later.",
        )

    if (
        form_data.username != settings.ADMIN_EMAIL
        or form_data.password != settings.ADMIN_PASSWORD
    ):
        attempts.append(datetime.now(timezone.utc))
        _ADMIN_LOGIN_ATTEMPTS[ip_address] = attempts
        log_login_attempt(form_data.username, success=False, ip_address=ip_address)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin email or password",
        )

    _ADMIN_LOGIN_ATTEMPTS[ip_address] = []
    log_login_attempt(form_data.username, success=True, ip_address=ip_address)

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": auth.create_access_token(
            settings.ADMIN_EMAIL,
            expires_delta=access_token_expires,
            role="admin",
            token_scope="access",
        ),
        "refresh_token": auth.create_refresh_token(settings.ADMIN_EMAIL, role="admin"),
        "token_type": "bearer",
    }


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    *,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request,
) -> Any:
    """Standard login for tenant users from database."""
    ip_address = request.client.host if request.client else "unknown"

    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        log_login_attempt(form_data.username, success=False, ip_address=ip_address)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not crud.user.is_active(user):
        log_login_attempt(form_data.username, success=False, ip_address=ip_address)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive. Contact administrator."
        )
    
    log_login_attempt(form_data.username, success=True, ip_address=ip_address)

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": auth.create_access_token(
            user.id, expires_delta=access_token_expires, role="user", token_scope="access"
        ),
        "refresh_token": auth.create_refresh_token(user.id, role="user"),
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=schemas.Token)
def refresh_access_token(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Depends(deps.reusable_oauth2),
) -> Any:
    """Refresh access token for admin or regular user."""
    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    role = payload.get("role")
    token_scope = payload.get("scope")
    if token_scope != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scope",
        )

    if role == "admin" and user_id == settings.ADMIN_EMAIL:
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": auth.create_access_token(
                settings.ADMIN_EMAIL,
                expires_delta=access_token_expires,
                role="admin",
                token_scope="access",
            ),
            "refresh_token": auth.create_refresh_token(settings.ADMIN_EMAIL, role="admin"),
            "token_type": "bearer",
        }

    if role != "user":
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": auth.create_access_token(
            user.id, expires_delta=access_token_expires, role="user", token_scope="access"
        ),
        "refresh_token": auth.create_refresh_token(user.id, role="user"),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Return currently authenticated regular user profile."""
    return current_user


@router.get("/admin/me", response_model=schemas.AdminMe)
def read_admin_me(
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    """Return currently authenticated admin profile."""
    return {"email": current_admin.email, "role": current_admin.role}