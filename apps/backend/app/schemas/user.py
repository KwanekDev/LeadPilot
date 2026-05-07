"""
User schemas
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


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
    tenant_id: Optional[int] = None
    tenant_name: Optional[str] = None
    tenant_domain: Optional[str] = None


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


class AdminMe(BaseModel):
    email: EmailStr
    role: str = "admin"


class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class AdminPasswordReset(BaseModel):
    password: str = Field(min_length=12, max_length=128)