from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.core.base import Base

# Database URL: Use environment variable for security (e.g., set DATABASE_URL in .env or deployment)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:PANKAJ1313@localhost:5432/edusnap"  # Fallback for dev; avoid hardcoding in production
)

# Create engine with PostgreSQL - Added pooling and echo for debugging
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Max connections in pool
    max_overflow=20,     # Extra connections if pool is full
    pool_pre_ping=True,  # Check connection health before use
    echo=False           # Set to True for SQL logging in dev
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models here to ensure tables are created (avoid circular imports by placing after Base definition)
from app.core import models  # noqa: E402
print("REGISTERED TABLES:", Base.metadata.tables)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")