"""
Customer endpoints
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customers
    """
    customers = crud.customer.get_multi_by_tenant(
        db, tenant_id=current_user.tenant_id, skip=skip, limit=limit
    )
    return customers


@router.post("/", response_model=schemas.Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: schemas.CustomerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new customer
    """
    customer = crud.customer.create(db, obj_in=customer_in)
    customer.tenant_id = current_user.tenant_id
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get customer by ID
    """
    customer = crud.customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return customer


@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: int,
    customer_in: schemas.CustomerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update customer
    """
    customer = crud.customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    customer = crud.customer.update(db, db_obj=customer, obj_in=customer_in)
    return customer


@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete customer
    """
    customer = crud.customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    customer = crud.customer.remove(db, id=customer_id)
    return customer