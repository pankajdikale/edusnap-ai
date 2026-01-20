import os
import pickle
import numpy as np
import cv2
import insightface
from sqlalchemy.orm import Session
from tkinter import Tk, filedialog
from backend.app.core.database import SessionLocal
from backend.app.core.models import Student

# Hide the Tkinter root window
Tk().withdraw()

# Initialize InsightFace
app = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))


def encode_face(image_path):
    """Encode a face image and return its embedding"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Could not read {image_path}")
        return None
    
    

    faces = app.get(img)
    if len(faces) == 0:
        print(f"⚠️ No face detected in {image_path}")
        return None

    embedding = faces[0].embedding
    return embedding / np.linalg.norm(embedding)  # normalize


def register_student():
    """Pick an image and save student info + face embedding in DB"""
    db: Session = SessionLocal()

    # Pick student image
    image_path = filedialog.askopenfilename(
        title="Select student image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if not image_path:
        print("❌ No image selected. Exiting.")
        return

    name = input("👤 Enter student's FULL name: ").strip()
    roll_no = input("🎓 Enter student's Roll No: ").strip()
    department = input("🏫 Enter department: ").strip() or "CSE"
    semester = input("📘 Enter semester: ").strip() or "5"

    print(f"⚙️ Encoding face for {name} ...")
    embedding = encode_face(image_path)
    if embedding is None:
        print("❌ Failed to encode face. Try another photo.")
        return

    student = Student(
        name=name,
        roll_no=roll_no,
        department=department,
        semester=semester,
        embedding=pickle.dumps(embedding)
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    db.close()

    print(f"✅ Student '{name}' (Roll: {roll_no}) added successfully!")


if __name__ == "__main__":
    print("🎉 Welcome to EduSnap AI Student Registration!")
    while True:
        register_student()
        more = input("➕ Add another student? (y/n): ").strip().lower()
        if more != "y":
            break

    print("\n✅ Student registration completed!")

# backend/app/core/register_students.py

import pickle
import numpy as np
import cv2
import insightface
from sqlalchemy.orm import Session
from tkinter import Tk, filedialog
from backend.app.core.database import SessionLocal
from backend.app.core.models import Student

# 🟢 Hide the Tkinter window
Tk().withdraw()

# 🧠 Load InsightFace model
app = insightface.app.FaceAnalysis(providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))


def encode_face(image_path):
    """Encodes a face and returns normalized embedding"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Cannot read image: {image_path}")
        return None

    faces = app.get(img)
    if not faces:
        print("⚠️ No face detected in this image.")
        return None

    embedding = faces[0].embedding
    embedding = embedding / np.linalg.norm(embedding)  # Normalize
    return embedding


def register_student():
    """Register one student and store embedding in PostgreSQL"""
    db: Session = SessionLocal()

    image_path = filedialog.askopenfilename(
        title="Select Student Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if not image_path:
        print("❌ No image selected.")
        return

    name = input("👤 Enter student's FULL name: ").strip()
    roll_no = input("🎓 Enter student's Roll No: ").strip()
    department = input("🏫 Enter department: ").strip() or "CSE"
    semester = input("📘 Enter semester: ").strip() or "7"

    print(f"⚙️ Encoding face for {name} ...")
    embedding = encode_face(image_path)
    if embedding is None:
        print("❌ Face encoding failed. Try another image.")
        db.close()
        return

    # 🔒 Store as binary data
    embedding_bytes = pickle.dumps(embedding)

    student = Student(
        name=name,
        roll_no=roll_no,
        department=department,
        semester=semester,
        embedding=embedding_bytes
    )

    try:
        db.add(student)
        db.commit()
        print(f"✅ Student '{name}' added successfully!")
    except Exception as e:
        db.rollback()
        print(f"⚠️ Error saving student: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🎉 Welcome to EduSnap AI Student Registration!")
    while True:
        register_student()
        more = input("➕ Add another student? (y/n): ").strip().lower()
        if more != "y":
            break
    print("\n✅ Registration complete!")
