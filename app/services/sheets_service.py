import json
import logging
import os
from typing import Any, Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.core.config import settings
from app.core.templates import sheet_row_for_lead
from app.models.client import Client
from app.models.lead import Lead

logger = logging.getLogger(__name__)


def _get_credentials_dict() -> Any:
    if settings.GOOGLE_CREDENTIALS_PATH.exists():
        with open(settings.GOOGLE_CREDENTIALS_PATH, "r", encoding="utf-8") as token_file:
            return json.load(token_file)

    if os.getenv("GOOGLE_CLIENT_EMAIL") and os.getenv("GOOGLE_PRIVATE_KEY"):
        return {
            "type": os.getenv("GOOGLE_TYPE", "service_account"),
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL", ""),
        }

    logger.error("Google Sheets credentials are not configured.")
    raise FileNotFoundError("Google Sheets credentials are not configured.")


def get_sheet_client():
    credentials = _get_credentials_dict()
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    return gspread.authorize(creds)


def _open_sheet(client: Client):
    sheet_name = client.sheet_name or settings.DEFAULT_SHEET_NAME
    sheet_client = get_sheet_client()
    if client.sheet_id:
        return sheet_client.open_by_key(client.sheet_id).worksheet(sheet_name)
    return sheet_client.open(settings.GOOGLE_SHEETS_NAME).worksheet(sheet_name)


def append_lead_row(client: Client, lead: Lead) -> None:
    try:
        sheet = _open_sheet(client)
        row = sheet_row_for_lead(lead.email, lead.name or "", lead.source or "", lead.message or "")
        sheet.append_row(row)
        logger.info("Added lead row to sheet for client %s: %s", client.name, lead.email)
    except Exception as error:
        logger.warning("Could not append lead row to Google Sheets for client %s: %s", client.name, error)


def append_status_update(client: Client, lead: Lead) -> None:
    try:
        sheet = _open_sheet(client)
        row = [
            lead.id,
            lead.email,
            lead.status,
            lead.followup_stage,
            lead.last_contact_at.isoformat() if lead.last_contact_at else "",
            lead.next_followup_at.isoformat() if lead.next_followup_at else "",
        ]
        sheet.append_row(row)
        logger.info("Appended status update for lead %s for client %s", lead.email, client.name)
    except Exception as error:
        logger.warning("Could not append status update to Google Sheets for client %s: %s", client.name, error)
