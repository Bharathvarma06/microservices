from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password[:72])  # 🔐 bcrypt-safe

def verify_password(password, hashed):
    return pwd_context.verify(password[:72], hashed)

def create_token(data: dict, expires: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
