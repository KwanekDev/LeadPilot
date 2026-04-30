from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (UniqueConstraint("email", "client_id", name="uq_client_email"),)

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    email = Column(String, index=True, nullable=False)
    name = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String, default="manual", nullable=False)
    status = Column(String, default="new", nullable=False)
    followup_stage = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_contact_at = Column(DateTime, nullable=True)
    next_followup_at = Column(DateTime, nullable=True)

    client = relationship("Client", back_populates="leads")

    def __repr__(self) -> str:
        return f"<Lead id={self.id} email={self.email!r} status={self.status!r} stage={self.followup_stage}>"
