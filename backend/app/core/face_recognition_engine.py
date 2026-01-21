
import numpy as np
import cv2
import insightface
import pickle
from backend.app.core.database import SessionLocal
from backend.app.core.models import Student
from sqlalchemy.orm import Session


# ✅ Helper to extract only first name
def get_first_name(full_name: str) -> str:
    """Return only the first name from full name"""
    if not full_name:
        return "Unknown"
    return full_name.strip().split()[0]


class FaceEncoder:
    def __init__(self):
        # Initialize InsightFace (RetinaFace + ArcFace)
        self.app = insightface.app.FaceAnalysis(
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def l2_normalize(self, x):
        return x / np.sqrt(np.sum(np.square(x)))

    def encode_image(self, image_bytes):
        """Encodes a face from an image (returns embedding vector)"""
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None:
            return None

        faces = self.app.get(img)
        if not faces:
            return None

        return self.l2_normalize(faces[0].embedding)


encoder = FaceEncoder()


def recognize_faces_from_image(image_path: str):
    """
    Detect & recognize student faces in a classroom image.
    Compare with stored embeddings in DB and return attendance list.
    """

    db: Session = SessionLocal()
    img = cv2.imread(image_path)
    if img is None:
        return []

    # Load all known student embeddings from DB
    students = db.query(Student).filter(Student.embedding.isnot(None)).all()
    if not students:
        db.close()
        return []

    known_embeddings = []
    known_names = []
    known_rolls = []

    for s in students:
        emb = pickle.loads(s.embedding)  # Pickle loading
        known_embeddings.append(emb)
        known_names.append(s.name)
        known_rolls.append(s.roll_no)

    known_embeddings = np.array(known_embeddings)
    db.close()

    # Detect faces from uploaded classroom image
    faces = encoder.app.get(img)
    threshold = 0.45  # tweak sensitivity

    recognized = []

    for face in faces:
        emb = encoder.l2_normalize(face.embedding)  # Normalize query embedding
        # Fixed: Proper cosine similarity (0-1 range)
        similarities = np.dot(known_embeddings, emb) / (np.linalg.norm(known_embeddings, axis=1) * np.linalg.norm(emb))
        idx = np.argmax(similarities)
        max_sim = similarities[idx]

        name, roll, status = "Unknown", "N/A", "Absent"
        if max_sim > threshold:
            name = known_names[idx]
            roll = known_rolls[idx]
            status = "Present"

            # ✅ Show only first name on bounding box
            first_name = get_first_name(name)

            bbox = face.bbox.astype(int)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(
                img, first_name, (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )
        else:
            # Unknown face
            bbox = face.bbox.astype(int)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
            cv2.putText(
                img, "Unknown", (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
            )

        recognized.append({"roll_no": roll, "name": name, "status": status})

    # ✅ Save preview with first-name labels (optional)
    output_path = image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(output_path, img)
    print(f"✅ Detected faces saved to: {output_path}")

    return recognized