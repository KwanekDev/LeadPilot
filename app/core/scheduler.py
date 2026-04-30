import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.followup_service import process_due_followups

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(
        process_due_followups,
        trigger="interval",
        minutes=1,
        next_run_time=datetime.utcnow(),
        id="lead_followup_check",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Lead follow-up scheduler started")
