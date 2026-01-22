"""
Initialize EduSnap AI Database
Creates all tables for PostgreSQL using SQLAlchemy models
"""

from app.core.database import engine, Base
from app.core import models

def init_db():
    print("🛠️ Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database setup complete! Tables created successfully.")

if __name__ == "__main__":
    init_db()
