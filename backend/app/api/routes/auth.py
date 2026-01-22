# backend/app/api/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.models import User
from app.core import security

router = APIRouter(tags=["Auth"])

# ✅ Login input (EMAIL + PASSWORD)
class LoginSchema(BaseModel):
    email: str
    password: str

# ✅ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ LOGIN API
@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    # 1️⃣ Find user by EMAIL
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 2️⃣ Verify password
    if not security.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3️⃣ Create JWT token with correct payload for frontend decoding
    token_data = {
        "sub": user.email,  # 'sub' set to email for user lookup
        "role": user.role,
        "user_id": user.id
    }
    access_token = security.create_access_token(token_data)

    # 4️⃣ Send response frontend expects (updated for compatibility)
    return {
        "token": access_token,  # Changed from "access_token" to "token"
        "user": {
            "email": user.email,
            "role": user.role,
            "name": user.name or ""  # Included user details in nested object
        }
    }

# ✅ LOGOUT API (optional: client-side token removal, but added for completeness)
@router.post("/logout")
def logout():
    # For stateless JWT, logout is handled client-side (remove token from localStorage)
    # If you implement token blacklisting in security.py, add logic here
    return {"message": "Logged out successfully"}