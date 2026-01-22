import os
import cv2
import pickle
import numpy as np
from datetime import date
from app.core.database import SessionLocal
from app.core.models import Student, Attendance
from app.core.face_recognition_engine import FaceEncoder

# Initialize face encoder
encoder = FaceEncoder()
db = SessionLocal()

# 📸 Step 1: Select classroom image
image_path = input("Enter classroom image path: ").strip()
if not os.path.exists(image_path):
    print("❌ Image not found.")
    exit()

img = cv2.imread(image_path)
if img is None:
    print("❌ Failed to read image.")
    exit()

# 🧠 Step 2: Load all known student embeddings from DB
students = db.query(Student).filter(Student.embedding.isnot(None)).all()
if not students:
    print("⚠️ No registered students with face data found.")
    exit()

known_embeddings, known_names, known_rolls = [], [], []
for s in students:
    emb = pickle.loads(s.embedding)
    known_embeddings.append(emb)
    known_names.append(s.name)
    known_rolls.append(s.roll_no)

known_embeddings = np.array(known_embeddings)
threshold = 0.45  # similarity threshold

# 🔍 Step 3: Detect faces in classroom photo
faces = encoder.app.get(img)
if not faces:
    print("⚠️ No faces detected in image.")
    exit()

recognized_today = []
today = date.today()

for face in faces:
    emb = encoder.l2_normalize(face.embedding)
    cosine_sim = np.dot(known_embeddings, emb)
    idx = np.argmax(cosine_sim)
    max_sim = cosine_sim[idx]

    if max_sim > threshold:
        roll = known_rolls[idx]
        name = known_names[idx]
        status = "Present"

        # 💾 Step 4: Save attendance to DB (avoid duplicates)
        already_marked = (
            db.query(Attendance)
            .filter(Attendance.student_id == students[idx].id, Attendance.date == today)
            .first()
        )

        if not already_marked:
            record = Attendance(
                student_id=students[idx].id,
                subject="AI Class",  # change later dynamically
                date=today,
                status=status
            )
            db.add(record)
            recognized_today.append(name)

        # ✏️ Show first name on image
        bbox = face.bbox.astype(int)
        first_name = name.split()[0]
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(img, first_name, (bbox[0], bbox[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        bbox = face.bbox.astype(int)
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
        cv2.putText(img, "Unknown", (bbox[0], bbox[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# ✅ Step 5: Commit changes
db.commit()
db.close()

# 🖼️ Show results
cv2.imshow("Detected Students - Attendance", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("\n✅ Attendance marked for:")
for n in recognized_today:
    print(f" - {n}")

print(f"\n🗓️ Date: {today}")
