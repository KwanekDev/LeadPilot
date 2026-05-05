"""
API v1 router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analytics, auth, customers, health, jobs, leads, reminders, users

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])