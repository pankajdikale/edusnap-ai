from datetime import date, timedelta
from backend.app.core.database import SessionLocal
from backend.app.core.models import Attendance


def delete_old_attendance(days: int = 10):
    db = SessionLocal()
    try:
        cutoff_date = date.today() - timedelta(days=days)

        deleted = (
            db.query(Attendance)
            .filter(Attendance.date < cutoff_date)
            .delete()
        )

        db.commit()
        return deleted
    finally:
        db.close()
