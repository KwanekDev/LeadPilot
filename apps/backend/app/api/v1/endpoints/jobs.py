"""
Job endpoints
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = Query(None, description="Filter by status"),
    customer_id: int = Query(None, description="Filter by customer"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve jobs
    """
    if status:
        jobs = crud.job.get_by_status(
            db, tenant_id=current_user.tenant_id, status=status, skip=skip, limit=limit
        )
    elif customer_id:
        jobs = crud.job.get_by_customer(
            db, customer_id=customer_id, skip=skip, limit=limit
        )
    else:
        jobs = crud.job.get_multi_by_tenant(
            db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
        )
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    job_in: schemas.JobCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new job
    """
    job = crud.job.create(db, obj_in=job_in)
    job.tenant_id = current_user.tenant_id
    job.created_by_id = current_user.id
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=schemas.Job)
def read_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job by ID
    """
    job = crud.job.get(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return job


@router.put("/{job_id}", response_model=schemas.Job)
def update_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    job_in: schemas.JobUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update job
    """
    job = crud.job.get(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    job = crud.job.update(db, db_obj=job, obj_in=job_in)
    return job


@router.delete("/{job_id}", response_model=schemas.Job)
def delete_job(
    *,
    db: Session = Depends(deps.get_db),
    job_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete job
    """
    job = crud.job.get(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    job = crud.job.remove(db, id=job_id)
    return job