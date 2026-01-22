# backend/app/api/routes/attendance.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
from fastapi.responses import FileResponse

from app.core.database import SessionLocal
from app.core.attendance_engine import mark_attendance_from_image, process_attendance_file
from app.core.deps import get_current_user
from app.core.models import User

router = APIRouter(tags=["Attendance"])
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))  # Project root (edusnapai/)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_and_mark(
    file: UploadFile = File(...),
    department: str = Form(...),  # Added for frontend
    year: str = Form(...),  # Added for frontend
    course: str = Form(...),  # Added for frontend
    subject: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload classroom image or CSV/XLSX → detect/process → mark attendance
    """
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty can upload attendance")

    # 📂 Upload directory
    upload_dir = os.path.join(BASE_DIR, "backend", "app", "static", "uploads")  # Absolute path
    os.makedirs(upload_dir, exist_ok=True)

    # 📸 Save file safely
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Check file type and process accordingly
    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # 🧠 Image-based attendance (original logic) - Pass new fields
        result = mark_attendance_from_image(
            image_path=file_path,
            subject=subject,
            department=department,  # Added
            year=year,  # Added
            course=course  # Added
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {
            "message": "✅ Attendance marked successfully",
            "subject": subject,
            "course": course,  # Added
            "marked_by": current_user.name,
            "date": result["date"],
            "present_count": result["present_count"],
            "present_students": result["present_students"],
            "output_image": result["output_image"],
            "csv_report": result.get("csv_report", ""),  # Added
            "pdf_report": result.get("pdf_report", "")
        }
    elif file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
        # 📄 File-based attendance (new for frontend)
        result = process_attendance_file(file, db, current_user.id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

@router.get("/results")
def get_attendance_results(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get attendance results for faculty (with student names and image) - Updated for frontend"""
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty can view results")
    
    from app.core.models import Attendance
    records = db.query(Attendance).filter(Attendance.marked_by == current_user.id).all()
    # Placeholder for image URL (assume latest upload)
    image_url = "/static/uploads/latest.jpg"  # Update with real logic if needed
    students = [{"name": r.student.name, "rollNumber": r.student.roll_no} for r in records if r.student]
    return {
        "image": image_url,
        "students": students
    }

# 📥 Download CSV Report
@router.get("/download/latest/csv")
def download_latest_csv(current_user=Depends(get_current_user)):
    """Download the latest CSV file."""
    csv_dir = os.path.join(BASE_DIR, "backend", "storage", "attendance_reports", "csv")  # Absolute path
    if not os.path.exists(csv_dir):
        raise HTTPException(status_code=404, detail="No CSV files found")
    
    files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    if not files:
        raise HTTPException(status_code=404, detail="No CSV files found")
    
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(csv_dir, f)))
    file_path = os.path.join(csv_dir, latest_file)
    
    return FileResponse(path=file_path, media_type="text/csv", filename=latest_file)

@router.get("/download/latest/pdf")
def download_latest_pdf(current_user=Depends(get_current_user)):
    """Download the latest PDF file."""
    pdf_dir = os.path.join(BASE_DIR, "backend", "storage", "attendance_reports", "pdf")  # Absolute path
    if not os.path.exists(pdf_dir):
        raise HTTPException(status_code=404, detail="No PDF files found")
    
    files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    if not files:
        raise HTTPException(status_code=404, detail="No PDF files found")
    
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(pdf_dir, f)))
    file_path = os.path.join(pdf_dir, latest_file)
    print(f"DEBUG: Downloading: {latest_file} at {os.path.getmtime(file_path)}")  # Debug
    return FileResponse(path=file_path, media_type="application/pdf", filename=latest_file)

@router.get("/latest-image")
def get_latest_image(current_user=Depends(get_current_user)):
    """Get the latest attendance output image."""
    image_dir = os.path.join(BASE_DIR, "backend", "app", "static", "attendance_outputs")  # Absolute path
    if not os.path.exists(image_dir):
        return {"image": ""}
    
    files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    if not files:
        return {"image": ""}
    
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(image_dir, f)))
    return {"image": latest_file}