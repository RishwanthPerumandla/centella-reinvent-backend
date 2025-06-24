# ./main.py
from fastapi import FastAPI
from src.routes import project, molecule, tasks

app = FastAPI(title="REINVENT 4 Molecular Platform", version="2.0")
app.include_router(project.router, prefix="/api/v1/projects", tags=["Project Management"])
app.include_router(molecule.router, prefix="/api/v1/molecule", tags=["Molecule Design"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Task Management"])

@app.get("/")
def root():
    return {"message": "REINVENT API is live."}