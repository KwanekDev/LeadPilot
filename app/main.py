from typing import Optional

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import get_db
from app.models.lead import Lead

# Create database tables if they do not yet exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LeadPilot API",
    description="Simple lead intake service for fast webhook and API handling.",
)
class LeadCreate(BaseModel):
    """Schema used to validate incoming lead creation requests."""

    email: str = Field(..., example="jane@example.com")
    name: Optional[str] = Field(None, example="Jane Doe")


class LeadCreateResponse(BaseModel):
    """Response returned after a lead is created successfully."""

    message: str
    lead_id: int


@app.post(
    "/leads/",
    response_model=LeadCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lead(lead_in: LeadCreate, db: Session = Depends(get_db)):
    existing_lead = db.query(Lead).filter_by(email=lead_in.email).first()
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A lead with that email already exists.",
        )
    
    lead = Lead(email=lead_in.email, name=lead_in.name)
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {"message": "Lead saved successfully.", "lead_id": lead.id}

@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "The application is running."}