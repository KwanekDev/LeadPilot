"""
Customer database model
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Customer(Base):
    """Customer model"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    equipment_installed = Column(Text)  # JSON string of equipment
    warranty_expiration = Column(DateTime(timezone=True))
    service_history = Column(Text)  # JSON string of service records
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="customers")
    jobs = relationship("Job", back_populates="customer")
    reminders = relationship("Reminder", back_populates="customer")

    @property
    def full_name(self) -> str:
        """Get customer's full name"""
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return f"<Customer {self.full_name}>"