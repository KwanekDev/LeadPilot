import time
import logging
from app.services.followup_service import process_due_followups

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leadpilot-worker")

def run_worker():
    logger.info("Worker started. Checking for due followups...")
    while True:
        try:
            process_due_followups()
        except Exception as e:
            logger.error(f"Error in worker loop: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    run_worker()