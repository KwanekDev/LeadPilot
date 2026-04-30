from typing import Optional, List
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.auth import get_admin, hash_password
from app.services.client_service import create_client
from app.core.database import SessionLocal
from app.models.admin import AdminUser

router = APIRouter(prefix="/api/admin", tags=["admin"])

class AdminCreateClient(BaseModel):
    name: str = Field(..., example="Client Name")
    company_name: Optional[str] = Field(None, example="Firma XYZ")
    email_user: Optional[str] = Field(None, example="client@gmail.com")
    smtp_host: Optional[str] = Field(None, example="smtp.gmail.com")
    smtp_port: Optional[int] = Field(None, example=465)

class AdminClientResponse(BaseModel):
    id: int
    name: str
    company_name: Optional[str]
    email_user: Optional[str]
    smtp_host: Optional[str]
    smtp_port: Optional[int]
    api_key: str

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminLoginResponse(BaseModel):
    token: str

class AdminCreateUser(BaseModel):
    email: str
    password: str

class AdminUserResponse(BaseModel):
    id: int
    email: str

@router.post("/login", response_model=AdminLoginResponse)
def login_admin(credentials: AdminLogin):
    with SessionLocal() as session:
        hashed_pw = hash_password(credentials.password)
        admin = session.query(AdminUser).filter(
            AdminUser.email == credentials.email,
            AdminUser.password_hash == hashed_pw
        ).first()
        
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        token = secrets.token_urlsafe(32)
        admin.session_token = token
        session.commit()
        return AdminLoginResponse(token=token)

@router.post("/users", response_model=AdminUserResponse)
def create_admin_user(data: AdminCreateUser, _: str = Depends(get_admin)):
    with SessionLocal() as session:
        if session.query(AdminUser).filter(AdminUser.email == data.email).first():
            raise HTTPException(status_code=400, detail="Admin already exists")
        
        new_admin = AdminUser(
            email=data.email,
            password_hash=hash_password(data.password)
        )
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)
        return AdminUserResponse(id=new_admin.id, email=new_admin.email)

@router.get("/users", response_model=List[AdminUserResponse])
def get_admin_users(_: str = Depends(get_admin)):
    with SessionLocal() as session:
        admins = session.query(AdminUser).all()
        return [AdminUserResponse(id=a.id, email=a.email) for a in admins]

@router.post("/clients", response_model=AdminClientResponse)
def create_new_client(client_data: AdminCreateClient, _: str = Depends(get_admin)):
    client, api_key = create_client(
        name=client_data.name,
        company_name=client_data.company_name,
        email_user=client_data.email_user,
        smtp_host=client_data.smtp_host,
        smtp_port=client_data.smtp_port,
    )
    return AdminClientResponse(
        id=client.id,
        name=client.name,
        company_name=client.company_name,
        email_user=client.email_user,
        smtp_host=client.smtp_host,
        smtp_port=client.smtp_port,
        api_key=api_key,
    )