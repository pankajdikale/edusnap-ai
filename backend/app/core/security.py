from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError  # Added JWTError for decoding
import os
from passlib.context import CryptContext

# ==============================
# 🔐 JWT & Password Config
# ==============================

# Load secret key from environment (recommended for production)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret-dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================
# 🔑 Password Utilities
# ==============================

def get_password_hash(password: str) -> str:
    # bcrypt accepts max 72 bytes, so truncate safely
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed one"""
    return pwd_context.verify(plain_password, hashed_password)

# ==============================
# 🧾 JWT Token Utilities
# ==============================

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    # Ensure payload includes 'sub' (email), 'role', 'user_id' for frontend compatibility
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict]:
    """Decode and validate JWT token. Returns payload dict or None if invalid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None  # Invalid/expired token