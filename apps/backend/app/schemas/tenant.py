"""
Tenant schemas
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class TenantBase(BaseModel):
    """Base tenant schema"""
    name: str
    domain: Optional[str] = None
    logo_url: Optional[str] = None
    timezone: str = "UTC"
    business_hours_start: str = "09:00"
    business_hours_end: str = "17:00"
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[EmailStr] = None
    smtp_tls: Optional[bool] = True
    lead_capture_slug: Optional[str] = None
    lead_capture_enabled: Optional[bool] = False


class TenantCreate(TenantBase):
    """Tenant creation schema"""
    pass


class TenantUpdate(TenantBase):
    """Tenant update schema"""
    is_active: Optional[bool] = None
    subscription_status: Optional[str] = None


class Tenant(TenantBase):
    """Tenant response schema"""
    id: int
    is_active: bool
    subscription_status: str

    class Config:
        from_attributes = True