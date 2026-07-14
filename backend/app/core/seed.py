from app.core.database import SessionLocal
from app.core.models import User
from app.core.security import get_password_hash


def seed_admin():
    db = SessionLocal()

    try:
        existing = db.query(User).filter(
            User.email == "pankaj@edusnapai.in"
        ).first()

        if existing:
            print("✅ Admin already exists")
            return

        admin = User(
            username="PANKAJ ADMIN",
            email="pankaj@edusnapai.in",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("✅ Default admin created")

    finally:
        db.close()
