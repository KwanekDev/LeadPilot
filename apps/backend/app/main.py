"""
LeadPilot Backend API
FastAPI application for HVAC company management
"""

import json
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

logger = logging.getLogger("leadpilot")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="LeadPilot - SaaS platform for HVAC companies",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raw_body = await request.body()
    body_text = raw_body.decode("utf-8", errors="replace") if raw_body else ""
    try:
        body_json = json.loads(body_text) if body_text else {}
    except json.JSONDecodeError:
        body_json = {"raw": body_text}

    errors = exc.errors()
    first_message = errors[0].get("msg", "Validation error") if errors else "Validation error"
    expected_schema = None
    if request.url.path.endswith("/api/v1/admin/users"):
        expected_schema = {"email": "EmailStr", "password": "string (min 12 chars)"}

    logger.warning(
        "[VALIDATION ERROR] path=%s method=%s body=%s errors=%s expected_schema=%s",
        request.url.path,
        request.method,
        body_json,
        errors,
        expected_schema,
    )

    return JSONResponse(
        status_code=422,
        content={"detail": f"Validation failed: {first_message}"},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "leadpilot-backend"}