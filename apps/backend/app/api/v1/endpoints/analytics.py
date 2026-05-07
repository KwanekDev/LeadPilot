"""
Analytics endpoints
"""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

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
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    tenant_id = current_user.tenant_id

    lead_status = db.query(
        models.Lead.status,
        func.count(models.Lead.id).label('count')
    ).filter(
        models.Lead.tenant_id == tenant_id
    ).group_by(models.Lead.status).all()

    total_leads = db.query(func.count(models.Lead.id)).filter(
        models.Lead.tenant_id == tenant_id
    ).scalar() or 0

    converted_leads = db.query(func.count(models.Lead.id)).filter(
        models.Lead.tenant_id == tenant_id,
        models.Lead.status == 'converted'
    ).scalar() or 0

    leads_this_month = db.query(func.count(models.Lead.id)).filter(
        models.Lead.tenant_id == tenant_id,
        models.Lead.created_at >= month_start
    ).scalar() or 0

    total_customers = db.query(func.count(models.Customer.id)).filter(
        models.Customer.tenant_id == tenant_id
    ).scalar() or 0

    customers_this_month = db.query(func.count(models.Customer.id)).filter(
        models.Customer.tenant_id == tenant_id,
        models.Customer.created_at >= month_start
    ).scalar() or 0

    job_status = db.query(
        models.Job.status,
        func.count(models.Job.id).label('count')
    ).filter(
        models.Job.tenant_id == tenant_id
    ).group_by(models.Job.status).all()

    active_jobs = db.query(func.count(models.Job.id)).filter(
        models.Job.tenant_id == tenant_id,
        ~models.Job.status.in_(['completed', 'cancelled'])
    ).scalar() or 0

    jobs_completed_this_month = db.query(func.count(models.Job.id)).filter(
        models.Job.tenant_id == tenant_id,
        models.Job.status == 'completed',
        models.Job.completed_date >= month_start
    ).scalar() or 0

    revenue_sum = db.query(func.coalesce(func.sum(models.Job.total_cost), 0)).filter(
        models.Job.tenant_id == tenant_id,
        models.Job.status == 'completed',
        models.Job.completed_date >= month_start
    ).scalar() or 0

    average_job_value = db.query(func.coalesce(func.avg(models.Job.total_cost), 0)).filter(
        models.Job.tenant_id == tenant_id,
        models.Job.status == 'completed'
    ).scalar() or 0

    total_reminders = db.query(func.count(models.Reminder.id)).filter(
        models.Reminder.tenant_id == tenant_id
    ).scalar() or 0

    return {
        'total_leads': int(total_leads),
        'total_customers': int(total_customers),
        'active_jobs': int(active_jobs),
        'active_reminders': int(total_reminders),
        'leads_this_month': int(leads_this_month),
        'customers_this_month': int(customers_this_month),
        'jobs_completed_this_month': int(jobs_completed_this_month),
        'revenue_this_month': float(revenue_sum) / 100.0,
        'average_job_value': float(average_job_value) / 100.0 if average_job_value else 0.0,
        'conversion_rate': float(converted_leads) / float(total_leads) * 100.0 if total_leads else 0.0,
        'lead_status': dict(lead_status),
        'job_status': dict(job_status),
    }