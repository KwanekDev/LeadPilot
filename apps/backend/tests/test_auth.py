"""
Test authentication
"""

import pytest
from sqlalchemy.orm import Session

from app import crud
from app.core.auth import verify_password
from app.schemas.user import UserCreate


def test_create_user(db: Session):
    """Test user creation"""
    user_in = UserCreate(
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session):
    """Test user authentication"""
    user_in = UserCreate(
        email="auth@example.com",
        password="password123"
    )
    user = crud.user.create(db, obj_in=user_in)

    authenticated_user = crud.user.authenticate(db, email="auth@example.com", password="password123")
    assert authenticated_user
    assert authenticated_user.id == user.id

    # Test wrong password
    wrong_auth = crud.user.authenticate(db, email="auth@example.com", password="wrong")
    assert wrong_auth is None


def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword"
    hashed = crud.user.user._model.hashed_password if hasattr(crud.user.user, '_model') else None

    # Since we're testing the function directly
    from app.core.auth import get_password_hash
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)