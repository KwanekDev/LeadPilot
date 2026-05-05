"""
Tenant database model for multi-tenancy
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Tenant(Base):
    """Tenant model for multi-tenancy"""

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, index=True)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    subscription_status = Column(String(50), default="trial")  # trial, active, suspended, cancelled
    timezone = Column(String(50), default="UTC")
    business_hours_start = Column(String(10), default="09:00")
    business_hours_end = Column(String(10), default="17:00")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Tenant {self.name}>"