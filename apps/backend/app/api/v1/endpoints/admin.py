"""Admin endpoints."""
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.logging_config import log_admin_access

router = APIRouter()


# =========================
# HEALTH
# =========================
@router.get("/health", response_model=dict)
def admin_health_check(
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    return {
        "status": "ok",
        "admin_email": current_admin.email,
        "timestamp": datetime.utcnow().isoformat(),
    }


# =========================
# USERS
# =========================
@router.post("/users", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.AdminUserCreate,
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    log_admin_access(current_admin.email, "CREATE_USER", f"email={user_in.email}")

    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    tenant_local = user_in.email.split("@")[0]
    tenant = crud.tenant.get_by_domain(db, domain=tenant_local)
    if not tenant:
        tenant = crud.tenant.create(
            db,
            obj_in=schemas.TenantCreate(
                name=tenant_local.title(),
                domain=tenant_local,
            ),
        )
    return crud.user.create(
        db,
        obj_in=schemas.UserCreate(
            email=user_in.email,
            password=user_in.password,
            tenant_id=tenant.id,
            role="user",
            is_active=True,
        ),
    )


@router.get("/users", response_model=List[schemas.User])
def list_users(
    *,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    log_admin_access(current_admin.email, "LIST_USERS", f"skip={skip}, limit={limit}")
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    *,
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.email == current_admin.email:
        raise HTTPException(status_code=400, detail="Cannot delete admin account")
    log_admin_access(current_admin.email, "DELETE_USER", f"user_id={user_id}")
    return crud.user.remove(db, id=user_id)


@router.put("/users/{user_id}/reset-password", response_model=schemas.User)
def reset_user_password(
    *,
    user_id: int,
    db: Session = Depends(deps.get_db),
    reset_in: schemas.AdminPasswordReset,
    current_admin: deps.AdminPrincipal = Depends(deps.get_current_admin),
) -> Any:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    log_admin_access(current_admin.email, "RESET_PASSWORD", f"user_id={user_id}")
    return crud.user.update(db, db_obj=user, obj_in={"password": reset_in.password})