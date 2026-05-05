"""
Job schemas
"""

from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    """Base job schema"""
    customer_id: int
    title: str
    description: Optional[str] = None
    status: str = "scheduled"
    priority: str = "medium"
    scheduled_date: Optional[str] = None
    completed_date: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    labor_cost: Optional[int] = None
    parts_cost: Optional[int] = None
    total_cost: Optional[int] = None
    assigned_to_id: Optional[int] = None
    photos: Optional[str] = None
    completion_notes: Optional[str] = None


class JobCreate(JobBase):
    """Job creation schema"""
    pass


class JobUpdate(JobBase):
    """Job update schema"""
    pass


class Job(JobBase):
    """Job response schema"""
    id: int
    tenant_id: int
    created_by_id: Optional[int] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True