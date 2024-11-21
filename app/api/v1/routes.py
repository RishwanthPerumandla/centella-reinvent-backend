from fastapi import APIRouter
from app.api.v1.auth_routes import auth_router

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

# Include authentication routes
router.include_router(auth_router, prefix="/auth")