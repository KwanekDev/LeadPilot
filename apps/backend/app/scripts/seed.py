"""
Database seeding script
"""

import logging

from sqlalchemy.orm import Session

from app.crud import tenant
from app.db.session import SessionLocal
from app.schemas.tenant import TenantCreate

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