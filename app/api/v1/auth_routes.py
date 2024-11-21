from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import create_user, authenticate_user, create_access_token

auth_router = APIRouter()

@auth_router.post("/signup", response_model=UserResponse, tags=["Authentication"])
def signup(user: UserCreate):
    db_user = create_user(user)
    return db_user

@auth_router.post("/login", tags=["Authentication"])
def login(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
