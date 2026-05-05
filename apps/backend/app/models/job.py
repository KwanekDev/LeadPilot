"""
Job/Installation database model
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Job(Base):
    """Job/Installation model"""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="scheduled")  # scheduled, in_progress, completed, cancelled
    priority = Column(String(20), default="medium")  # low, medium, high
    scheduled_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    labor_cost = Column(Integer)  # in cents
    parts_cost = Column(Integer)  # in cents
    total_cost = Column(Integer)  # in cents
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    photos = Column(Text)  # JSON array of photo URLs
    completion_notes = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="jobs")
    customer = relationship("Customer", back_populates="jobs")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    created_by = relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<Job {self.title}>"