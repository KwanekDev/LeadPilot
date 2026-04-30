from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.auth import get_current_client
from app.core.database import get_db
from app.models.client import Client
from app.models.lead import Lead
from app.core.email import send_email
from app.services.followup_service import initialize_lead_followup, send_initial_response

router = APIRouter(tags=["leads"])

class LeadCreate(BaseModel):
    email: str = Field(..., example="test@mail.com")
    name: Optional[str] = Field(None, example="Jan")
    source: Optional[str] = Field("manual", example="manual")
    message: Optional[str] = Field(None, example="Szukam mieszkania 2 pokoje")

class LeadResponse(BaseModel):
    status: str
    lead_id: int

class LeadRead(BaseModel):
    id: int
    name: Optional[str]
    email: str
    message: Optional[str]
    source: str
    status: str
    followup_stage: int
    created_at: datetime
    last_contact_at: Optional[datetime]
    next_followup_at: Optional[datetime]

    class Config:
        orm_mode = True

class ReplyRequest(BaseModel):
    lead_id: int = Field(..., example=1)
    subject: Optional[str] = Field("Odpowiedź na Twoje zapytanie", example="Odpowiedź na Twoje zapytanie")
    message: str = Field(..., example="Dzień dobry, przesyłam ofertę...")

class LeadUpdate(BaseModel):
    email: Optional[str] = Field(None, example="test@mail.com")
    name: Optional[str] = Field(None, example="Jan")
    source: Optional[str] = Field(None, example="manual")
    message: Optional[str] = Field(None, example="Szukam mieszkania 2 pokoje")

@router.post(
    "/lead",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
@router.post(
    "/leads/",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lead(
    lead: LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    existing_lead = db.query(Lead).filter(Lead.email == lead.email, Lead.client_id == client.id).first()
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lead with this email already exists for this client.",
        )

    new_lead = Lead(
        email=lead.email,
        name=lead.name,
        source=lead.source,
        message=lead.message,
        status="new",
        created_at=datetime.utcnow(),
        client_id=client.id,
    )
    initialize_lead_followup(new_lead, client)
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    background_tasks.add_task(send_initial_response, new_lead, client)

    return LeadResponse(status="ok", lead_id=new_lead.id)

@router.get(
    "/leads",
    response_model=List[LeadRead],
)
def list_leads(
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    leads = db.query(Lead).filter(Lead.client_id == client.id).order_by(Lead.created_at.desc()).all()
    return leads

@router.get(
    "/leads/{lead_id}",
    response_model=LeadRead,
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client.id).one_or_none()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead

@router.patch("/leads/{lead_id}", response_model=LeadRead)
def update_lead(
    lead_id: int,
    update_data: LeadUpdate,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client.id).one_or_none()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    lead.name = update_data.name or lead.name
    lead.email = update_data.email or lead.email
    lead.source = update_data.source or lead.source
    lead.message = update_data.message or lead.message
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.delete("/leads/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client.id).one_or_none()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"status": "deleted"}

@router.post(
    "/reply",
    response_model=LeadResponse,
)
def reply_lead(
    reply: ReplyRequest,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    lead = db.query(Lead).filter(Lead.id == reply.lead_id, Lead.client_id == client.id).one_or_none()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    success = send_email(
        lead.email,
        reply.subject,
        reply.message,
        smtp_user=client.email_user,
        smtp_password_encrypted=client.email_password_encrypted,
        smtp_host=client.smtp_host,
        smtp_port=client.smtp_port,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to send reply email.",
        )

    lead.status = "replied"
    lead.last_contact_at = datetime.utcnow()
    lead.next_followup_at = None
    db.add(lead)
    db.commit()

    return LeadResponse(status="replied", lead_id=lead.id)

@router.get("/ping")
def ping():
    return {"status": "LeadPilot is available"}