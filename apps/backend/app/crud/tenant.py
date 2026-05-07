"""
Tenant CRUD operations
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    """Tenant CRUD operations"""

    def get_by_domain(self, db: Session, *, domain: str) -> Optional[Tenant]:
        """Get tenant by domain"""
        return db.query(Tenant).filter(Tenant.domain == domain).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Tenant]:
        """Get tenant by public lead capture slug"""
        return db.query(Tenant).filter(Tenant.lead_capture_slug == slug).first()


tenant = CRUDTenant(Tenant)