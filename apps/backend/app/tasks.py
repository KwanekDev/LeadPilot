"""
Celery tasks
"""

from datetime import datetime

from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app import crud
from app.utils.email import send_email
from app.utils.sms import send_sms


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
                    if settings.ENABLE_SMS:
                        send_sms_reminder.delay(reminder.id)
                    else:
                        print(f"SMS disabled, skipping SMS reminder {reminder.id}")
                elif reminder.channel == "both":
                    send_email_reminder.delay(reminder.id)
                    if settings.ENABLE_SMS:
                        send_sms_reminder.delay(reminder.id)
                    else:
                        print(f"SMS disabled, skipping SMS part of reminder {reminder.id}")

                # Update reminder next date
                crud.reminder.update_next_reminder_date(db, db_obj=reminder)
    finally:
        db.close()


@celery_app.task
def send_email_reminder(reminder_id: int):
    """Send email reminder"""
    db = SessionLocal()
    try:
        reminder = crud.reminder.get(db, id=reminder_id)
        if not reminder:
            print(f"Reminder {reminder_id} not found")
            return

        customer = crud.customer.get(db, id=reminder.customer_id)
        if not customer:
            print(f"Customer {reminder.customer_id} not found for reminder {reminder_id}")
            return

        if not customer.email:
            print(f"Customer {customer.id} has no email address")
            return

        # Create email content
        subject = f"Maintenance Reminder: {reminder.title}"
        body = f"""
        <html>
        <body>
            <h2>{reminder.title}</h2>
            <p>Dear {customer.first_name or 'Valued Customer'},</p>
            <p>{reminder.description or 'This is your scheduled maintenance reminder.'}</p>
            <p>Please contact us to schedule your service.</p>
            <br>
            <p>Best regards,<br>LeadPilot Team</p>
        </body>
        </html>
        """

        tenant = crud.tenant.get(db, id=customer.tenant_id)
        smtp_settings = {
            "smtp_server": getattr(tenant, "smtp_server", None),
            "smtp_port": getattr(tenant, "smtp_port", None),
            "smtp_username": getattr(tenant, "smtp_username", None),
            "smtp_password": getattr(tenant, "smtp_password", None),
            "smtp_tls": getattr(tenant, "smtp_tls", None),
        }
        from_email = tenant.smtp_from_email if tenant and tenant.smtp_from_email else None

        success = send_email(
            to_email=customer.email,
            subject=subject,
            body=body,
            from_email=from_email,
            **smtp_settings,
        )

        if success:
            # Update reminder sent count
            reminder.sent_count += 1
            db.commit()
            print(f"Email reminder sent for reminder {reminder_id}")
        else:
            print(f"Failed to send email reminder for reminder {reminder_id}")

    except Exception as e:
        print(f"Error sending email reminder {reminder_id}: {str(e)}")
    finally:
        db.close()


@celery_app.task
def send_sms_reminder(reminder_id: int):
    """Send SMS reminder"""
    db = SessionLocal()
    try:
        reminder = crud.reminder.get(db, id=reminder_id)
        if not reminder:
            print(f"Reminder {reminder_id} not found")
            return

        customer = crud.customer.get(db, id=reminder.customer_id)
        if not customer:
            print(f"Customer {reminder.customer_id} not found for reminder {reminder_id}")
            return

        if not customer.phone:
            print(f"Customer {customer.id} has no phone number")
            return

        # Create SMS content
        message = f"Maintenance Reminder: {reminder.title}. {reminder.description or 'Please contact us to schedule your service.'}"

        # Send SMS
        success = send_sms(
            to_phone=customer.phone,
            message=message
        )

        if success:
            # Update reminder sent count
            reminder.sent_count += 1
            db.commit()
            print(f"SMS reminder sent for reminder {reminder_id}")
        else:
            print(f"Failed to send SMS reminder for reminder {reminder_id}")

    except Exception as e:
        print(f"Error sending SMS reminder {reminder_id}: {str(e)}")
    finally:
        db.close()


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