# backend/app/api/routes/admin.py
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.core import models, security
from backend.app.core.deps import get_current_user

router = APIRouter(tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas ---
class FacultyCreate(BaseModel):
    username: str
    email: EmailStr
    name: str  # Added for frontend compatibility
    department: Optional[str] = None
    year: Optional[str] = None
    password: str

class FacultyOut(BaseModel):
    id: int
    name: str  # Changed from username to name
    email: EmailStr
    department: Optional[str] = None
    year: Optional[str] = None

    class Config:
        orm_mode = True

# ✅ Dashboard overview (Admin only)
@router.get("/dashboard")
def get_dashboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    total_students = db.query(models.Student).count()
    total_faculty = db.query(models.User).filter(models.User.role == "faculty").count()
    total_attendance = db.query(models.Attendance).count()
    
    return {
        "totalStudents": total_students,
        "totalFaculty": total_faculty,
        "totalAttendanceRecords": total_attendance
    }

# ✅ Reports (Admin only) - Updated for frontend compatibility
@router.get("/reports")
def get_reports(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Fetch attendance records with student/course details; calculate attendance %
    reports = db.query(models.Attendance).join(models.Student).limit(10).all()  # Limit for demo; expand as needed
    return [
        {
            "course": r.course,  # From updated models.py
            "attendance": "85%",  # Placeholder: Calculate real % based on status
            "date": str(r.date)
        }
        for r in reports
    ]

# ✅ Test Route (open)
@router.get("/ping")
def ping_admin():
    return {"message": "Admin route working (only accessible by admin in real app)"}

# ✅ Add new faculty (Admin only)
@router.post(
    "/add-faculty",
    status_code=status.HTTP_201_CREATED,
)
def add_faculty(payload: FacultyCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_pw = security.get_password_hash(payload.password)
    faculty = models.User(
        username=payload.username,
        email=payload.email,
        name=payload.name,  # Added
        role="faculty",
        hashed_password=hashed_pw,
        department=payload.department,
        year=payload.year,
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    return {"message": f"Faculty '{payload.name}' added successfully 🎉", "id": faculty.id}

# ✅ Get all faculty members (Admin only)
@router.get("/faculty", response_model=List[FacultyOut])
def get_faculty(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    faculties = db.query(models.User).filter(models.User.role == "faculty").all()
    return [
        {
            "id": f.id,
            "name": f.name,  # Changed from username
            "email": f.email,
            "department": getattr(f, "department", None),
            "year": getattr(f, "year", None),
        }
        for f in faculties
    ]

# ✅ Delete a faculty by email and password (Admin only) - Updated for frontend compatibility
@router.delete("/delete-faculty")
def delete_faculty(payload: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    faculty = db.query(models.User).filter(
        models.User.email == email, models.User.role == "faculty"
    ).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    # Verify password before deleting
    if not security.verify_password(password, faculty.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    db.delete(faculty)
    db.commit()
    return {"message": "Faculty deleted successfully ✅"}