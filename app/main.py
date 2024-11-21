from fastapi import FastAPI
from app.api.v1.routes import router as v1_router
from app.db.base import Base
from app.db.session import engine


app = FastAPI()

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Centella Reinvent Backend"}
