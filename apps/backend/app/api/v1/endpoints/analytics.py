"""
Analytics endpoints
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_analytics(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dashboard analytics
    """
    # Lead stats
    lead_stats = db.query(
        models.Lead.status,
        func.count(models.Lead.id).label('count')
    ).filter(
        models.Lead.tenant_id == current_user.tenant_id
    ).group_by(models.Lead.status).all()

    # Customer stats
    customer_count = crud.customer.get_multi_by_tenant(
        db, tenant_id=current_user.tenant_id
    ).__len__()

    # Job stats
    job_stats = db.query(
        models.Job.status,
        func.count(models.Job.id).label('count')
    ).filter(
        models.Job.tenant_id == current_user.tenant_id
    ).group_by(models.Job.status).all()

    # Reminder stats
    reminder_count = crud.reminder.get_multi_by_tenant(
        db, tenant_id=current_user.tenant_id
    ).__len__()

    return {
        "leads": dict(lead_stats),
        "customers": {"total": customer_count},
        "jobs": dict(job_stats),
        "reminders": {"total": reminder_count},
    }