import logging
from fastapi import FastAPI, Depends, BackgroundTasks, Security
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from app.database import engine, Base, get_db
from app.models.lead import Lead
from app.services.email import send_email
from app.core.config import get_api_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
scheduler = BackgroundScheduler()

def followup_job(email: str, name: str) -> None:
    """Send a follow-up email one day after lead creation."""
    content = f"Cześć {name}, wracam do tematu. Czy udało Ci się zapoznać z ofertą?"
    success = send_email(email, "Pytanie o ofertę", content)
    if success:
        logger.info(f"Follow-up email sent to {email}")
    else:
        logger.warning(f"Failed to send follow-up email to {email}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/leads/", dependencies=[Depends(get_api_key)])
def handle_new_lead(email: str, name: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Create a new lead and schedule welcome and follow-up emails."""
    if db.query(Lead).filter(Lead.email == email).first():
        logger.warning(f"Lead with email {email} already exists")
        return {"status": "exists"}

    lead = Lead(email=email, name=name)
    db.add(lead)
    db.commit()
    logger.info(f"Lead created: {email} ({name})")

    background_tasks.add_task(send_email, email, "Dzięki za kontakt", f"Hej {name}, odezwiemy się!")
    logger.info(f"Welcome email scheduled for {email}")
    scheduler.add_job(
        followup_job, 
        'date', 
        run_date=datetime.now() + timedelta(days=1),
        args=[email, name]
    )
    logger.info(f"Follow-up email scheduled for {email} in 1 day")

    return {"status": "ok"}