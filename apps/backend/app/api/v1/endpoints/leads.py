"""
Lead endpoints
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Lead])
def read_leads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = Query(None, description="Filter by status"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve leads
    """
    if status:
        leads = crud.lead.get_by_status(
            db, tenant_id=current_user.tenant_id, status=status, skip=skip, limit=limit
        )
    else:
        leads = crud.lead.get_multi_by_tenant(
            db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
        )
    return leads


@router.post("/", response_model=schemas.Lead)
def create_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.LeadCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new lead
    """
    lead_data = lead_in.model_dump(exclude_unset=True)
    lead_data["tenant_id"] = current_user.tenant_id
    lead_data["created_by_id"] = current_user.id
    lead_data["source"] = lead_data.get("source") or "app"
    lead = crud.lead.create(db, obj_in=schemas.LeadCreate(**lead_data))
    return lead


@router.get("/{lead_id}", response_model=schemas.Lead)
def read_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get lead by ID
    """
    lead = crud.lead.get(db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return lead


@router.put("/{lead_id}", response_model=schemas.Lead)
def update_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    lead_in: schemas.LeadUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update lead
    """
    lead = crud.lead.get(db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    lead = crud.lead.update(db, db_obj=lead, obj_in=lead_in)
    return lead


@router.delete("/{lead_id}", response_model=schemas.Lead)
def delete_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete lead
    """
    lead = crud.lead.get(db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    lead = crud.lead.remove(db, id=lead_id)
    return lead