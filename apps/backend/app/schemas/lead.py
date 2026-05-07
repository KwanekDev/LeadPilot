"""
Lead schemas
"""

from typing import Optional

from pydantic import BaseModel


class LeadBase(BaseModel):
    """Base lead schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: str = "new"
    source: Optional[str] = None
    notes: Optional[str] = None
    estimated_value: Optional[int] = None
    assigned_to_id: Optional[int] = None
    tenant_id: Optional[int] = None
    created_by_id: Optional[int] = None


class LeadCreate(LeadBase):
    """Lead creation schema"""
    pass


class LeadUpdate(LeadBase):
    """Lead update schema"""
    pass


class Lead(LeadBase):
    """Lead response schema"""
    id: int
    tenant_id: int
    created_by_id: Optional[int] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True