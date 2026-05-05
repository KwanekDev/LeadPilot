"""
Reminder schemas
"""

from typing import Optional

from pydantic import BaseModel


class ReminderBase(BaseModel):
    """Base reminder schema"""
    customer_id: int
    title: str
    description: Optional[str] = None
    reminder_type: str = "maintenance"
    interval_months: int = 6
    next_reminder_date: Optional[str] = None
    last_reminder_date: Optional[str] = None
    is_active: bool = True
    channel: str = "email"
    template: Optional[str] = None


class ReminderCreate(ReminderBase):
    """Reminder creation schema"""
    pass


class ReminderUpdate(ReminderBase):
    """Reminder update schema"""
    pass


class Reminder(ReminderBase):
    """Reminder response schema"""
    id: int
    tenant_id: int
    sent_count: int = 0
    created_by_id: Optional[int] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True