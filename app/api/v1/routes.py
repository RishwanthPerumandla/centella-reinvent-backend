from fastapi import APIRouter, Depends
from app.services.auth_service import auth_middleware
from app.api.v1.auth_routes import auth_router

router = APIRouter()

# Public Route
@router.get("/health")
def health_check():
    return {"status": "ok"}

# Protected Route
@router.get("/protected")
def protected_route(user: dict = Depends(auth_middleware)):
    return {"message": f"Hello, {user['sub']}! This is a protected route."}

# Include authentication routes
router.include_router(auth_router, prefix="/auth")
