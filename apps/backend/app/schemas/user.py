"""
User schemas
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    role: str = "user"


class UserCreate(UserBase):
    """User creation schema"""
    password: str


class UserUpdate(UserBase):
    """User update schema"""
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """User in database base schema"""
    id: int
    tenant_id: Optional[int] = None
    is_superuser: bool = False

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """User response schema"""
    pass


class UserInDB(UserInDBBase):
    """User in database schema"""
    hashed_password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None