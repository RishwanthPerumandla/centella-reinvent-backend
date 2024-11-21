from passlib.context import CryptContext
from jose import jwt
from app.models.user_model import User
from app.db.session import SessionLocal
from app.schemas.user_schema import UserCreate

# Configurations
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from app.core.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

def auth_middleware(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded JWT payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Password Hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Token Generation
def create_access_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# User Management
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None
