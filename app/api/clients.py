from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.auth import get_current_client
from app.models.client import Client
from app.core.database import SessionLocal
from app.models.lead import Lead

router = APIRouter(prefix="/api/client", tags=["client"])

class ClientConfig(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    welcome_subject: Optional[str] = None
    welcome_body: Optional[str] = None
    followup_1_subject: Optional[str] = None
    followup_1_body: Optional[str] = None
    followup_2_subject: Optional[str] = None
    followup_2_body: Optional[str] = None
    followup_1_delay_hours: Optional[int] = None
    followup_2_delay_hours: Optional[int] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    company_name: Optional[str]
    email_user: Optional[str]
    smtp_host: Optional[str]
    smtp_port: Optional[int]
    welcome_subject: Optional[str]
    welcome_body: Optional[str]
    followup_1_subject: Optional[str]
    followup_1_body: Optional[str]
    followup_2_subject: Optional[str]
    followup_2_body: Optional[str]
    followup_1_delay_hours: int
    followup_2_delay_hours: int

@router.get("/me", response_model=ClientResponse)
def get_client_info(client: Client = Depends(get_current_client)):
    return ClientResponse(
        id=client.id,
        name=client.name,
        company_name=client.company_name,
        email_user=client.email_user,
        smtp_host=client.smtp_host,
        smtp_port=client.smtp_port,
        welcome_subject=client.welcome_subject,
        welcome_body=client.welcome_body,
        followup_1_subject=client.followup_1_subject,
        followup_1_body=client.followup_1_body,
        followup_2_subject=client.followup_2_subject,
        followup_2_body=client.followup_2_body,
        followup_1_delay_hours=client.followup_1_delay_hours,
        followup_2_delay_hours=client.followup_2_delay_hours,
    )

@router.patch("/me", response_model=ClientResponse)
def update_client_config(
    config: ClientConfig,
    client: Client = Depends(get_current_client),
):
    updates = config.dict(exclude_none=True)
    with SessionLocal() as session:
        db_client = session.query(Client).filter(Client.id == client.id).one_or_none()
        if not db_client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        for key, value in updates.items():
            if key == "email_password":
                from app.core.security import encrypt_value
                value = encrypt_value(value)
                setattr(db_client, "email_password_encrypted", value)
            else:
                setattr(db_client, key, value)
        db_client.updated_at = datetime.utcnow()
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return ClientResponse(
            id=db_client.id,
            name=db_client.name,
            company_name=db_client.company_name,
            email_user=db_client.email_user,
            smtp_host=db_client.smtp_host,
            smtp_port=db_client.smtp_port,
            welcome_subject=db_client.welcome_subject,
            welcome_body=db_client.welcome_body,
            followup_1_subject=db_client.followup_1_subject,
            followup_1_body=db_client.followup_1_body,
            followup_2_subject=db_client.followup_2_subject,
            followup_2_body=db_client.followup_2_body,
            followup_1_delay_hours=db_client.followup_1_delay_hours,
            followup_2_delay_hours=db_client.followup_2_delay_hours,
        )

@router.get("/export/leads")
def export_leads_csv(client: Client = Depends(get_current_client)):
    with SessionLocal() as session:
        leads = session.query(Lead).filter(Lead.client_id == client.id).order_by(Lead.created_at.desc()).all()
    lines = ["id,email,name,source,status,followup_stage,created_at,last_contact_at,next_followup_at"]
    for lead in leads:
        lines.append(
            ",".join(
                [
                    str(lead.id),
                    lead.email,
                    lead.name or "",
                    lead.source or "",
                    lead.status,
                    str(lead.followup_stage),
                    lead.created_at.isoformat() if lead.created_at else "",
                    lead.last_contact_at.isoformat() if lead.last_contact_at else "",
                    lead.next_followup_at.isoformat() if lead.next_followup_at else "",
                ]
            )
        )
    return {"csv": "\n".join(lines)}