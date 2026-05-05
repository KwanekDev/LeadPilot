"""
Customer schemas
"""

from typing import Optional

from pydantic import BaseModel


class CustomerBase(BaseModel):
    """Base customer schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    equipment_installed: Optional[str] = None
    warranty_expiration: Optional[str] = None
    service_history: Optional[str] = None
    is_active: bool = True


class CustomerCreate(CustomerBase):
    """Customer creation schema"""
    pass


class CustomerUpdate(CustomerBase):
    """Customer update schema"""
    pass


class Customer(CustomerBase):
    """Customer response schema"""
    id: int
    tenant_id: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True