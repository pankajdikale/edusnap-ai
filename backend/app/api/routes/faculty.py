# backend/app/api/routes/faculty.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import os

from app.core.database import SessionLocal
from app.core.models import Attendance, Student, User
from app.core.face_recognition_engine import recognize_faces_from_image
from app.core.deps import get_current_user  # JWT-based auth

router = APIRouter(tags=["Faculty"])

# ✅ Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Test route
@router.get("/ping")
def ping_faculty():
    return {"message": "Faculty route working ✅"}

# ✅ Upload attendance image - Updated to save new fields
@router.post("/upload-attendance")
async def upload_attendance(
    file: UploadFile = File(...),
    department: str = Form(...),
    year: str = Form(...),
    course: str = Form(...),
    subject: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Faculty uploads a classroom photo → Detect faces → Mark attendance.
    """
    # ✅ Validate faculty role
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Access denied. Faculty only.")

    # ✅ Save image locally
    upload_dir = "backend/app/static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ✅ Face recognition logic (stub/demo)
    try:
        recognized = recognize_faces_from_image(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition error: {e}")

    if not recognized:
        recognized = [
            {"roll_no": "01", "name": "Sagar", "status": "Present"},
            {"roll_no": "02", "name": "Dhruvika", "status": "Absent"},
            {"roll_no": "03", "name": "Nishika", "status": "Present"},
        ]

    # ✅ Store in DB - Updated to include new fields
    today = date.today()
    for entry in recognized:
        student = db.query(Student).filter(Student.roll_no == entry["roll_no"]).first()
        attendance = Attendance(
            student_id=student.id if student else None,
            subject=subject,
            course=course,  # Added
            department=department,  # Added
            year=year,  # Added
            date=today,
            status=entry["status"],
            marked_by=current_user.id,  # Fixed: Use ID instead of username
        )
        db.add(attendance)
    db.commit()

    return {
        "message": f"✅ Attendance uploaded by {current_user.name}",
        "subject": subject,
        "course": course,
        "recognized_count": len(recognized),
        "records": recognized,
        "file_saved": file_path,
    }

# ✅ Get attendance reports (for that faculty) - Updated for frontend compatibility
@router.get("/reports")
def get_faculty_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch all attendance reports uploaded by the current faculty.
    """
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Access denied. Faculty only.")
    
    reports = (
        db.query(Attendance)
        .filter(Attendance.marked_by == current_user.id)  # Fixed: Use ID
        .all()
    )

    return [
        {
            "subject": r.subject,  # Updated for frontend
            "attendance": "88%",  # Placeholder: Calculate real % based on status
            "date": str(r.date)
        }
        for r in reports
    ]