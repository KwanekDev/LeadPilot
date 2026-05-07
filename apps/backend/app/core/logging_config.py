"""
Logging utilities
"""

import logging
from datetime import datetime

logger = logging.getLogger("leadpilot")


def log_admin_access(admin_email: str, action: str, details: str = "") -> None:
    """
    Log admin access attempts and actions.
    """
    timestamp = datetime.utcnow().isoformat()
    message = f"[ADMIN ACCESS] {timestamp} - Admin: {admin_email} - Action: {action}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)


def log_login_attempt(email: str, success: bool, ip_address: str = "") -> None:
    """
    Log login attempts.
    """
    timestamp = datetime.utcnow().isoformat()
    status = "SUCCESS" if success else "FAILED"
    message = f"[LOGIN] {timestamp} - Email: {email} - Status: {status}"
    if ip_address:
        message += f" - IP: {ip_address}"
    if success:
        logger.info(message)
    else:
        logger.warning(message)
