"""
Reminder CRUD operations
"""

from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate


class CRUDReminder(CRUDBase[Reminder, ReminderCreate, ReminderUpdate]):
    """Reminder CRUD operations"""

    def get_multi_by_tenant(
        self, db: Session, *, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> List[Reminder]:
        """Get multiple reminders by tenant"""
        return (
            db.query(self.model)
            .filter(Reminder.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_due_reminders(self, db: Session, *, tenant_id: int) -> List[Reminder]:
        """Get reminders that are due for sending"""
        now = datetime.utcnow()
        return (
            db.query(self.model)
            .filter(
                Reminder.tenant_id == tenant_id,
                Reminder.is_active == True,
                Reminder.next_reminder_date <= now
            )
            .all()
        )

    def update_next_reminder_date(self, db: Session, *, db_obj: Reminder) -> Reminder:
        """Update the next reminder date based on interval"""
        if db_obj.is_active and db_obj.interval_months:
            next_date = db_obj.next_reminder_date or datetime.utcnow()
            db_obj.next_reminder_date = next_date + timedelta(days=30 * db_obj.interval_months)
            db_obj.sent_count += 1
            db_obj.last_reminder_date = datetime.utcnow()
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj


reminder = CRUDReminder(Reminder)