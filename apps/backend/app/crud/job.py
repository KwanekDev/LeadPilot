"""
Job CRUD operations
"""

from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    """Job CRUD operations"""

    def get_multi_by_tenant(
        self, db: Session, *, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        """Get multiple jobs by tenant"""
        return (
            db.query(self.model)
            .filter(Job.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, tenant_id: int, status: str, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        """Get jobs by status"""
        return (
            db.query(self.model)
            .filter(Job.tenant_id == tenant_id, Job.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_customer(
        self, db: Session, *, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        """Get jobs by customer"""
        return (
            db.query(self.model)
            .filter(Job.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


job = CRUDJob(Job)