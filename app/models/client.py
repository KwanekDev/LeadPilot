from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    api_key_hash = Column(String, unique=True, nullable=False, index=True)
    email_user = Column(String, nullable=True)
    email_password_encrypted = Column(Text, nullable=True)
    smtp_host = Column(String, nullable=True)
    smtp_port = Column(Integer, nullable=True)
    welcome_subject = Column(String, nullable=True)
    welcome_body = Column(Text, nullable=True)
    followup_1_subject = Column(String, nullable=True)
    followup_1_body = Column(Text, nullable=True)
    followup_2_subject = Column(String, nullable=True)
    followup_2_body = Column(Text, nullable=True)
    followup_1_delay_hours = Column(Integer, default=24, nullable=False)
    followup_2_delay_hours = Column(Integer, default=48, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    leads = relationship("Lead", back_populates="client")