"""
Base database models
"""

from app.db.session import Base

# Import all models to ensure they are registered with SQLAlchemy
from app.models import Tenant, User  # noqa: F401