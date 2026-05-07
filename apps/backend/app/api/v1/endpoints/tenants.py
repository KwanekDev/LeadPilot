"""
Tenant endpoints
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/settings/me", response_model=schemas.Tenant)
def get_tenant_settings(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get current tenant settings"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant = crud.tenant.get(db, id=current_user.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/settings/me", response_model=schemas.Tenant)
def update_tenant_settings(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: schemas.TenantUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update current tenant settings"""
    if not current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant = crud.tenant.get(db, id=current_user.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    if tenant_in.lead_capture_slug and tenant_in.lead_capture_slug != tenant.lead_capture_slug:
        existing = crud.tenant.get_by_slug(db, slug=tenant_in.lead_capture_slug)
        if existing and existing.id != tenant.id:
            raise HTTPException(status_code=400, detail="This lead capture slug is already in use.")

    updated = crud.tenant.update(db, db_obj=tenant, obj_in=tenant_in)
    return updated
