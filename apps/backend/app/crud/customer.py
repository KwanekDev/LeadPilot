"""
Customer CRUD operations
"""

from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    """Customer CRUD operations"""

    def get_multi_by_tenant(
        self, db: Session, *, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> List[Customer]:
        """Get multiple customers by tenant"""
        return (
            db.query(self.model)
            .filter(Customer.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


customer = CRUDCustomer(Customer)