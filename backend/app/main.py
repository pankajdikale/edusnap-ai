from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import students
from backend.app.core.database import engine
from backend.app.core import models
from backend.app.api.routes import auth, admin, faculty, attendance, reports
from backend.app.core.attendance_cleanup import delete_old_attendance

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduSnap AI - Backend")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Explicit origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Include OPTIONS for preflight
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
templates = Jinja2Templates(directory="backend/app/templates")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(faculty.router, prefix="/api/faculty", tags=["Faculty"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])

@app.get("/")
def home():
    return {"message": "Welcome to EduSnap AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "Backend is connected successfully 🚀"}

@app.on_event("startup")
def startup_tasks():
    delete_old_attendance(days=10)