import logging
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.email import send_email
from app.core.templates import (
    DEFAULT_FOLLOWUP_1_BODY,
    DEFAULT_FOLLOWUP_1_SUBJECT,
    DEFAULT_FOLLOWUP_2_BODY,
    DEFAULT_FOLLOWUP_2_SUBJECT,
    DEFAULT_WELCOME_BODY,
    DEFAULT_WELCOME_SUBJECT,
    render_template,
)
from app.models.client import Client
from app.models.lead import Lead

logger = logging.getLogger(__name__)

def build_next_followup_time(stage: int, client: Client) -> Optional[datetime]:
    if stage == 0:
        return datetime.utcnow() + timedelta(hours=client.followup_1_delay_hours)
    if stage == 1:
        return datetime.utcnow() + timedelta(hours=client.followup_2_delay_hours)
    return None

def initialize_lead_followup(lead: Lead, client: Client) -> None:
    lead.status = "new"
    lead.followup_stage = 0
    lead.last_contact_at = datetime.utcnow()
    lead.next_followup_at = build_next_followup_time(0, client)

def send_initial_response(lead: Lead, client: Client) -> bool:
    subject = client.welcome_subject or DEFAULT_WELCOME_SUBJECT
    body = render_template(client.welcome_body, DEFAULT_WELCOME_BODY, lead.name or "Kliencie", client.company_name or "Zespół")
    success = send_email(
        lead.email,
        subject,
        body,
        smtp_user=client.email_user,
        smtp_password_encrypted=client.email_password_encrypted,
        smtp_host=client.smtp_host,
        smtp_port=client.smtp_port,
    )
    return success

def send_followup(lead: Lead, client: Client) -> bool:
    if lead.followup_stage == 0:
        subject = client.followup_1_subject or DEFAULT_FOLLOWUP_1_SUBJECT
        body = render_template(client.followup_1_body, DEFAULT_FOLLOWUP_1_BODY, lead.name or "Kliencie", client.company_name or "Zespół")
    elif lead.followup_stage == 1:
        subject = client.followup_2_subject or DEFAULT_FOLLOWUP_2_SUBJECT
        body = render_template(client.followup_2_body, DEFAULT_FOLLOWUP_2_BODY, lead.name or "Kliencie", client.company_name or "Zespół")
    else:
        return False

    success = send_email(
        lead.email,
        subject,
        body,
        smtp_user=client.email_user,
        smtp_password_encrypted=client.email_password_encrypted,
        smtp_host=client.smtp_host,
        smtp_port=client.smtp_port,
    )
    if not success:
        lead.next_followup_at = datetime.utcnow() + timedelta(hours=1)
        return False

    lead.last_contact_at = datetime.utcnow()
    lead.followup_stage += 1

    if lead.followup_stage == 1:
        lead.next_followup_at = build_next_followup_time(1, client)
    else:
        lead.next_followup_at = None
        lead.status = "cold"

    return True

def process_due_followups() -> None:
    now = datetime.utcnow()
    with SessionLocal() as db:
        leads = (
            db.query(Lead)
            .filter(Lead.next_followup_at != None)
            .filter(Lead.next_followup_at <= now)
            .filter(Lead.status == "new")
            .all()
        )

        for lead in leads:
            client = db.query(Client).filter(Client.id == lead.client_id).one_or_none()
            if not client or not client.enabled:
                continue
            send_followup(lead, client)
            db.add(lead)
        db.commit()