from fastapi import FastAPI
from src.routes import molecule, tasks

app = FastAPI(title="REINVENT Molecular Design API", version="1.0")

# Registering API routes
app.include_router(molecule.router, prefix="/api/v1/molecule", tags=["Molecule Design"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Task Management"])

@app.get("/")
def root():
    return {"message": "REINVENT API is running!"}
