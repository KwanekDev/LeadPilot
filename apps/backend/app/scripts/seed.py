"""
Database seeding script
"""

import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import tenant, user
from app.db.session import SessionLocal
from app.schemas.tenant import TenantCreate
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database(db: Session) -> None:
    """Seed database with initial data"""

    # Create default tenant
    default_tenant = tenant.get_by_domain(db, domain="default")
    if not default_tenant:
        tenant_in = TenantCreate(
            name="Default Company",
            domain="default",
        )
        default_tenant = tenant.create(db, obj_in=tenant_in)
        logger.info(f"Created default tenant: {default_tenant.name}")

    # Create admin user
    admin_user = user.get_by_email(db, email=settings.ADMIN_EMAIL)
    if not admin_user:
        user_in = UserCreate(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            first_name="Admin",
            last_name="User",
            is_superuser=True,
            role="admin",
        )
        admin_user = user.create(db, obj_in=user_in)
        admin_user.tenant_id = default_tenant.id
        db.commit()
        logger.info(f"Created admin user: {admin_user.email}")

    logger.info("Database seeding completed")


def main() -> None:
    """Main seeding function"""
    logger.info("Starting database seeding...")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()