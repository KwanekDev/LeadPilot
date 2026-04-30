from app.core.database import Base, engine, SessionLocal
from app.models.admin import AdminUser
from app.core.auth import hash_password
from app.models.client import Client
from app.models.lead import Lead

def setup_admin():
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        email = "banapio51@gmail.com"
        password = "8813553"
        
        existing = session.query(AdminUser).filter(AdminUser.email == email).first()
        if not existing:
            admin = AdminUser(
                email=email,
                password_hash=hash_password(password)
            )
            session.add(admin)
            session.commit()
            print(f"Utworzono glownego administratora: {email}")
        else:
            print(f"Administrator {email} juz istnieje.")

if __name__ == "__main__":
    setup_admin()