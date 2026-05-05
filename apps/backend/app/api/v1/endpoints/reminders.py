"""
Reminder endpoints
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Reminder])
def read_reminders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve reminders
    """
    reminders = crud.reminder.get_multi_by_tenant(
        db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
    return reminders


@router.post("/", response_model=schemas.Reminder)
def create_reminder(
    *,
    db: Session = Depends(deps.get_db),
    reminder_in: schemas.ReminderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new reminder
    """
    reminder = crud.reminder.create(db, obj_in=reminder_in)
    reminder.tenant_id = current_user.tenant_id
    reminder.created_by_id = current_user.id
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("/{reminder_id}", response_model=schemas.Reminder)
def read_reminder(
    *,
    db: Session = Depends(deps.get_db),
    reminder_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get reminder by ID
    """
    reminder = crud.reminder.get(db, id=reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if reminder.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return reminder


@router.put("/{reminder_id}", response_model=schemas.Reminder)
def update_reminder(
    *,
    db: Session = Depends(deps.get_db),
    reminder_id: int,
    reminder_in: schemas.ReminderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update reminder
    """
    reminder = crud.reminder.get(db, id=reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if reminder.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    reminder = crud.reminder.update(db, db_obj=reminder, obj_in=reminder_in)
    return reminder


@router.delete("/{reminder_id}", response_model=schemas.Reminder)
def delete_reminder(
    *,
    db: Session = Depends(deps.get_db),
    reminder_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete reminder
    """
    reminder = crud.reminder.get(db, id=reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if reminder.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    reminder = crud.reminder.remove(db, id=reminder_id)
    return reminder