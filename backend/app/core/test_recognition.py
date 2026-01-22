# backend/app/core/test_recognition.py

import os
import pickle
import numpy as np
import cv2
import insightface
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.models import Student
from tkinter import Tk, filedialog
from app.core.face_recognition_engine import recognize_faces_from_image
# Hide Tkinter main window
Tk().withdraw()

# Load InsightFace model
print("🚀 Loading model...")
app = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
print("✅ Model loaded successfully!\n")

# Select test image (e.g., classroom photo or individual photo)
image_path = filedialog.askopenfilename(
    title="Select a test image (classroom or student photo)",
    filetypes=[("Image files", "*.jpg *.jpeg *.png")]
)
if not image_path or not os.path.exists(image_path):
    print("❌ No image selected or invalid file path.")
    exit()

# Load image
img = cv2.imread(image_path)
if img is None:
    print("❌ Failed to read the selected image.")
    exit()

# Get all students with embeddings from DB
db: Session = SessionLocal()
students = db.query(Student).filter(Student.embedding.isnot(None)).all()

if not students:
    print("⚠️ No students with embeddings found in DB.")
    db.close()
    exit()

known_embeddings = []
known_names = []
for s in students:
    emb = pickle.loads(s.embedding)  # Pickle loading
    known_embeddings.append(emb)
    known_names.append(s.name)

known_embeddings = np.array(known_embeddings)
print(f"📚 Loaded {len(known_names)} registered student embeddings.\n")

# Detect faces in the image
faces = app.get(img)
print(f"🧠 Detected {len(faces)} face(s) in the image.\n")

threshold = 0.45  # adjust if needed
for i, face in enumerate(faces):
    emb = face.embedding / np.linalg.norm(face.embedding)  # Normalize query embedding
    # Fixed: Proper cosine similarity (0-1 range)
    similarities = np.dot(known_embeddings, emb) / (np.linalg.norm(known_embeddings, axis=1) * np.linalg.norm(emb))
    idx = np.argmax(similarities)
    max_sim = similarities[idx]
    
    if max_sim > threshold:
        name = known_names[idx]
        print(f"✅ Face #{i+1} recognized as: {name} (Similarity: {max_sim:.2f})")
        color = (0, 255, 0)
        label = name.split()[0]
    else:
        name = "Unknown"
        print(f"❌ Face #{i+1} not recognized (Similarity: {max_sim:.2f})")
        color = (0, 0, 255)
        label = "Unknown"

    # Draw bounding box and name
    bbox = face.bbox.astype(int)
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
    cv2.putText(img, label, (bbox[0], bbox[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

# 🧾 Save and show output
output_path = os.path.join(os.getcwd(), "recognized_output.jpg")
cv2.imwrite(output_path, img)
print(f"\n✅ Output saved as: {output_path}")

try:
    cv2.imshow("Detected Faces", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except cv2.error:
    print("⚠️ Display not supported. Please open recognized_output.jpg manually.")
