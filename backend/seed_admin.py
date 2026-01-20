from backend.app.core.database import SessionLocal
from backend.app.core import models
from backend.app.core.security import get_password_hash
from backend.app.core.models import User

def seed_admin():
    db = SessionLocal()

    existing = db.query(models.User).filter(
        models.User.username == "PANKAJ ADMIN"
    ).first()

    if existing:
        print("⚠️ Admin already exists")
        return

    hashed = get_password_hash("admin123")

    admin = models.User(
        username="PANKAJ ADMIN",
        email="pankaj@edusnapai.in",
        hashed_password=hashed,
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("✅ Admin user created successfully")

if __name__ == "__main__":
    seed_admin()
