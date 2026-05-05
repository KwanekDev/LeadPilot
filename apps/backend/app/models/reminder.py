"""
Reminder database model
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Reminder(Base):
    """Reminder model"""

    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50), default="maintenance")  # maintenance, follow_up, warranty
    interval_months = Column(Integer, default=6)  # months between reminders
    next_reminder_date = Column(DateTime(timezone=True))
    last_reminder_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    channel = Column(String(20), default="email")  # email, sms, both
    template = Column(Text)  # reminder message template
    sent_count = Column(Integer, default=0)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="reminders")
    customer = relationship("Customer", back_populates="reminders")
    created_by = relationship("User")

    def __repr__(self):
        return f"<Reminder {self.title}>"