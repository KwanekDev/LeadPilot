"""
Lead database model
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Lead(Base):
    """Lead model"""

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    status = Column(String(50), default="new")  # new, contacted, qualified, converted, lost
    source = Column(String(100))  # website, referral, phone, etc.
    notes = Column(Text)
    estimated_value = Column(Integer)  # in cents
    created_by_id = Column(Integer, ForeignKey("users.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="leads")
    created_by = relationship("User", foreign_keys=[created_by_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])

    @property
    def full_name(self) -> str:
        """Get lead's full name"""
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return f"<Lead {self.full_name}>"