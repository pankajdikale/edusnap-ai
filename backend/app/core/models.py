from sqlalchemy import Column, Integer, String, LargeBinary, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)  # Used for login
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="faculty")  # Supports "admin", "faculty", "student"
    name = Column(String(120), nullable=True)  # Added: Required for frontend login response

    department = Column(String(50), nullable=True)
    year = Column(String(10), nullable=True)

    attendances_marked = relationship("Attendance", back_populates="marked_by_user")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)  # Used in attendance results
    roll_no = Column(String(50), unique=True, nullable=False)
    department = Column(String(50), nullable=True)
    semester = Column(String(10), nullable=True)

    # 🧠 Face embedding stored as binary data (512D vector)
    embedding = Column(LargeBinary, nullable=True)

    # Relationships
    attendance_records = relationship("Attendance", back_populates="student")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    course = Column(String(100), nullable=False)  # Added: For frontend upload
    department = Column(String(50), nullable=False)  # Added: For filtering
    year = Column(String(10), nullable=False)  # Added: For frontend upload
    date = Column(Date, nullable=False)
    status = Column(String(20), default="Present")

    # Who marked this attendance (faculty from User)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    marked_by_user = relationship("User", back_populates="attendances_marked")