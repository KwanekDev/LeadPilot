"""
Authentication endpoints
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import auth
from app.core.config import settings

router = APIRouter()

# Definiujemy schemat dla tokena, aby móc go ręcznie wyciągnąć w refreshu
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token"
)

@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": auth.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": auth.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/refresh-token", response_model=schemas.Token)
def refresh_access_token(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Depends(reusable_oauth2), # Używamy surowego tokena, nie current_user
) -> Any:
    """
    Refresh access token. 
    Ten endpoint przyjmuje Refresh Token w nagłówku Authorization.
    """
    # 1. Dekodujemy token ręcznie, aby sprawdzić użytkownika (używając funkcji z core.auth)
    # Zakładamy, że auth.decode_token lub auth.verify_token istnieje w Twoim systemie
    user_id = auth.verify_token(token) 
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": auth.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": auth.create_refresh_token(user.id), # Opcjonalnie generujemy nowy refresh
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user
    """
    return current_user