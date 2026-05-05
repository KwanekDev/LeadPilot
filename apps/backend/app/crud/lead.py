"""
Lead CRUD operations
"""

from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate


class CRUDLead(CRUDBase[Lead, LeadCreate, LeadUpdate]):
    """Lead CRUD operations"""

    def get_multi_by_tenant(
        self, db: Session, *, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> List[Lead]:
        """Get multiple leads by tenant"""
        return (
            db.query(self.model)
            .filter(Lead.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, tenant_id: int, status: str, skip: int = 0, limit: int = 100
    ) -> List[Lead]:
        """Get leads by status"""
        return (
            db.query(self.model)
            .filter(Lead.tenant_id == tenant_id, Lead.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )


lead = CRUDLead(Lead)