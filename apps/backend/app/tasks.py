"""
Celery tasks
"""

from datetime import datetime

from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app import crud


@celery_app.task
def send_reminders():
    """Send due reminders"""
    db = SessionLocal()
    try:
        # Get all tenants
        tenants = crud.tenant.get_multi(db)
        for tenant in tenants:
            if not tenant.is_active:
                continue

            # Get due reminders for this tenant
            due_reminders = crud.reminder.get_due_reminders(db, tenant_id=tenant.id)
            for reminder in due_reminders:
                # Send reminder based on channel
                if reminder.channel == "email":
                    send_email_reminder.delay(reminder.id)
                elif reminder.channel == "sms":
                    send_sms_reminder.delay(reminder.id)
                elif reminder.channel == "both":
                    send_email_reminder.delay(reminder.id)
                    send_sms_reminder.delay(reminder.id)

                # Update reminder next date
                crud.reminder.update_next_reminder_date(db, db_obj=reminder)
    finally:
        db.close()


@celery_app.task
def send_email_reminder(reminder_id: int):
    """Send email reminder"""
    # TODO: Implement email sending
    print(f"Sending email reminder for reminder {reminder_id}")


@celery_app.task
def send_sms_reminder(reminder_id: int):
    """Send SMS reminder"""
    # TODO: Implement SMS sending
    print(f"Sending SMS reminder for reminder {reminder_id}")


@celery_app.task
def process_lead_conversion(lead_id: int):
    """Process lead conversion to customer"""
    db = SessionLocal()
    try:
        lead = crud.lead.get(db, id=lead_id)
        if lead and lead.status == "converted":
            # Create customer from lead
            customer_in = {
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "email": lead.email,
                "phone": lead.phone,
                "address": lead.address,
            }
            customer = crud.customer.create(db, obj_in=customer_in)
            customer.tenant_id = lead.tenant_id
            db.commit()
            db.refresh(customer)
            print(f"Converted lead {lead_id} to customer {customer.id}")
    finally:
        db.close()