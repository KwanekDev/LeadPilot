"""Public endpoints for lead capture and forms."""
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()
_PUBLIC_FORM_ATTEMPTS: dict[str, list[datetime]] = {}
_PUBLIC_MAX_REQUESTS = 30
_PUBLIC_WINDOW_SECONDS = 300


def _prune_attempts(attempts: list[datetime]) -> list[datetime]:
    now = datetime.now(timezone.utc)
    return [ts for ts in attempts if (now - ts).total_seconds() <= _PUBLIC_WINDOW_SECONDS]


@router.post("/form/{form_slug}", response_model=schemas.Lead)
def submit_public_lead(
    form_slug: str,
    lead_in: schemas.LeadCreate,
    request: Request,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Submit a public lead from a form capture URL"""
    ip_address = request.client.host if request.client else "unknown"
    throttle_key = f"{ip_address}:{form_slug}"
    attempts = _prune_attempts(_PUBLIC_FORM_ATTEMPTS.get(throttle_key, []))
    if len(attempts) >= _PUBLIC_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")
    attempts.append(datetime.now(timezone.utc))
    _PUBLIC_FORM_ATTEMPTS[throttle_key] = attempts

    tenant = crud.tenant.get_by_slug(db, slug=form_slug)
    if not tenant or not tenant.lead_capture_enabled:
        raise HTTPException(status_code=404, detail="Form not found")

    lead_data = lead_in.model_dump(exclude_unset=True)
    lead_data["tenant_id"] = tenant.id
    lead_data["source"] = lead_data.get("source") or "web_form"
    lead = crud.lead.create(db, obj_in=schemas.LeadCreate(**lead_data))
    return lead
