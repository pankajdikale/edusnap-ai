# backend/app/api/routes/reports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from backend.app.core.deps import get_current_user
from backend.app.core.database import SessionLocal
from backend.app.core.models import Attendance

router = APIRouter(tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin")
def get_admin_reports(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    ✅ Admin reports: All attendance records with summary.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    reports = db.query(Attendance).all()
    return [
        {
            "course": r.course,  # From updated models
            "attendance": "85%",  # Placeholder: Calculate real % (e.g., based on status counts)
            "date": str(r.date)
        }
        for r in reports
    ]

@router.get("/faculty")
def get_faculty_reports(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    ✅ Faculty reports: Only their uploaded attendance.
    """
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Access denied")
    
    reports = db.query(Attendance).filter(Attendance.marked_by == current_user.id).all()
    print(f"Debug: Faculty {current_user.id} has {len(reports)} attendance records")  # Debug print
    
    return [
        {
            "subject": r.subject,
            "attendance": "88%",  # Placeholder: Calculate real % if needed
            "date": str(r.date)
        }
        for r in reports
    ]

@router.get("/download/{filename}")
def download_report(filename: str):
    """
    ✅ Returns a direct file download from attendance_reports folder.
    """

    # Decide folder based on file type
    if filename.endswith(".pdf"):
        file_path = os.path.join("backend", "storage", "attendance_reports", "pdf", filename)
    elif filename.endswith(".csv"):
        file_path = os.path.join("backend", "storage", "attendance_reports", "csv", filename)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    from fastapi.responses import FileResponse
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=filename
    )
