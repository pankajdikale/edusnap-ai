from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import SessionLocal
from app.core.models import User

# Define OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # Updated to match prefixed endpoint

# Database dependency
def get_db():
    """Provides a SQLAlchemy session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Extract current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode JWT token and return the current user"""
    payload = security.decode_access_token(token)  # Use centralized decode function from security.py
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    email: str = payload.get("sub")  # 'sub' is set to email in create_access_token
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
    
    user = db.query(User).filter(User.email == email).first()  # Query by email, not username
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user