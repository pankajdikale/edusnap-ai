import os
import cv2
import pickle
import numpy as np
import pandas as pd  # Added for CSV/XLSX processing
from datetime import date
from backend.app.core.database import SessionLocal
from backend.app.core.models import Student, Attendance, User
from backend.app.core.face_recognition_engine import FaceEncoder
from backend.app.core.attendance_report import generate_csv, generate_pdf

encoder = FaceEncoder()

BASE_DIR = os.path.abspath(os.getcwd())
OUTPUT_DIR = os.path.join(BASE_DIR, "backend", "storage", "attendance_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_attendance_file(file, db, faculty_id):
    """Process uploaded CSV/XLSX file for attendance marking (for frontend upload)."""
    try:
        # Read file based on extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Unsupported file type. Use CSV or XLSX."}

        # Assume columns: roll_no, status (Present/Absent), subject (optional)
        required_cols = ['roll_no', 'status']
        if not all(col in df.columns for col in required_cols):
            return {"error": "File must have 'roll_no' and 'status' columns."}

        today = date.today()
        subject = df.get('subject', ['General'])[0]  # Default subject if not provided
        processed_count = 0

        for _, row in df.iterrows():
            roll_no = row['roll_no']
            status = row['status'].capitalize()  # Ensure 'Present' or 'Absent'

            # Find student by roll_no
            student = db.query(Student).filter(Student.roll_no == roll_no).first()
            if not student:
                continue  # Skip unknown students

            # Check if already marked
            existing = db.query(Attendance).filter(
                Attendance.student_id == student.id,
                Attendance.subject == subject,
                Attendance.date == today
            ).first()
            if existing:
                continue  # Skip duplicates

            # Add attendance record (note: course/department/year not used in file processing, so defaults)
            db.add(Attendance(
                student_id=student.id,
                subject=subject,
                course="General",  # Default for file uploads
                department="General",  # Default for file uploads
                year=str(today.year),  # Default to current year
                date=today,
                status=status,
                marked_by=faculty_id
            ))
            processed_count += 1

        db.commit()
        return {"message": f"Attendance processed for {processed_count} students.", "processed": processed_count}

    except Exception as e:
        db.rollback()
        return {"error": f"Failed to process file: {str(e)}"}

def mark_attendance_from_image(image_path: str, subject: str, department: str = "", year: str = "", course: str = ""):
    """Original image-based attendance marking (preserved for face recognition). Updated to accept new params and fixed similarity."""
    db = SessionLocal()
    today = date.today()

    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Invalid image"}

    students = db.query(Student).filter(Student.embedding.isnot(None)).all()
    if not students:
        return {"error": "No registered faces found"}

    known_embeddings = []
    student_map = {}

    for idx, s in enumerate(students):
        try:
            emb = pickle.loads(s.embedding)  # Pickle loading
            known_embeddings.append(emb)
            student_map[idx] = s
        except Exception as e:
            print(f"Skipping invalid embedding for {s.name}: {e}")
            continue

    known_embeddings = np.array(known_embeddings)

    faces = encoder.app.get(img)
    threshold = 0.45

    present_students = []

    for face in faces:
        emb = encoder.l2_normalize(face.embedding)  # Normalize query embedding
        # Fixed: Proper cosine similarity (0-1 range)
        similarities = np.dot(known_embeddings, emb) / (np.linalg.norm(known_embeddings, axis=1) * np.linalg.norm(emb))
        idx = np.argmax(similarities)
        max_sim = similarities[idx]

        if max_sim > threshold:
            student = student_map[idx]

            already_marked = db.query(Attendance).filter(
                Attendance.student_id == student.id,
                Attendance.subject == subject,
                Attendance.date == today
            ).first()

            if not already_marked:
                db.add(Attendance(
                    student_id=student.id,
                    subject=subject,
                    course=course,  # Added
                    department=department,  # Added
                    year=year,  # Added
                    date=today,
                    status="Present"
                ))

            present_students.append({
                "id": student.id,
                "roll_no": student.roll_no,
                "name": student.name,
                "department": student.department
            })

            label = student.name.split()[0]
            color = (0, 255, 0)
        else:
            label = "Unknown"
            color = (0, 0, 255)

        bbox = face.bbox.astype(int)
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        cv2.putText(img, label, (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    output_image = os.path.join("backend", "app", "static", "attendance_outputs", f"{subject}_{today}.jpg")
    cv2.imwrite(output_image, img)

    db.commit()
    db.close()

    csv_path = generate_csv(subject, present_students)
    pdf_path = generate_pdf(subject, present_students)

    return {
    "date": str(today),
    "subject": subject,
    "present_count": len(present_students),
    "present_students": present_students,
    "output_image": os.path.basename(output_image),
    "csv_report": os.path.basename(csv_path),  # Just filename, e.g., "cloud_2026-01-19.csv"
    "pdf_report": os.path.basename(pdf_path)   # Just filename, e.g., "cloud_2026-01-19.pdf"
     }