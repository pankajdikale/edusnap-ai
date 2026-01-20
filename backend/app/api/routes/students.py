# backend/app/api/routes/students.py
import os
import pickle
import cv2
import numpy as np
import insightface
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.core.models import Student

router = APIRouter(tags=["Students"])

# Load face model once
face_app = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
async def add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    department: str = Form(...),  # Made required to match frontend
    semester: str = Form(...),    # Made required to match frontend
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check for existing roll_no
    existing = db.query(Student).filter(Student.roll_no == roll_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Roll number already exists")
    
    # 1️⃣ Save uploaded image locally (optional)
    os.makedirs("backend/app/static/student_images", exist_ok=True)
    image_path = f"backend/app/static/student_images/{roll_no}.jpg"
    contents = await image.read()
    with open(image_path, "wb") as f:
        f.write(contents)

    # 2️⃣ Read and detect face with error handling
    try:
        img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        faces = face_app.get(img)
        if not faces:
            raise HTTPException(status_code=400, detail="No face detected in image")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {e}")

    # 3️⃣ Get face embedding
    emb = faces[0].embedding.astype("float32")
    emb_bytes = pickle.dumps(emb)  # Pickle storage

    # 4️⃣ Save student in DB
    student = Student(
        name=name,
        roll_no=roll_no,
        department=department,
        semester=semester,
        embedding=emb_bytes
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"message": f"✅ Added {name}", "student_id": student.id}