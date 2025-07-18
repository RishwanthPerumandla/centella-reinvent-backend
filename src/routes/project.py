#  routes/project.py
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
from src.services.project_service import create_project_dir, save_smiles_file
from src.tasks.transfer_learning import run_transfer_learning_task
from src.tasks.reinforcement_learning import run_reinforcement_learning_task
from src.tasks.generation import run_sampling_from_agent
from src.db.connection import SessionLocal
from src.db.models import Job
from typing import List

router = APIRouter()
PROJECT_ROOT = Path("/app/projects")

@router.post("/")
def create_project():
    project_id = str(uuid.uuid4())
    try:
        create_project_dir(project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"project_id": project_id, "message": "Project created."}

@router.post("/{project_id}/upload")
def upload_smiles_file(project_id: str, file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    try:
        save_smiles_file(project_id, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"project_id": project_id, "message": "SMILES file uploaded."}

@router.post("/{project_id}/train")
async def train_model(project_id: str):
    try:
        run_transfer_learning_task.delay(project_id)  # ✅ send to Celery
        return {"project_id": project_id, "status": "training_queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/reinforce")
def reinforce_model(project_id: str):
    try:
        run_reinforcement_learning_task.delay(project_id)  # ✅ Use Celery queue
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reinforcement learning failed: {str(e)}")
    return {"project_id": project_id, "status": "reinforcement_queued"}



@router.post("/{project_id}/generate")
def generate_molecules(project_id: str):
    try:
        run_sampling_from_agent.delay(project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    return {"project_id": project_id, "status": "generation_queued"}


@router.get("/{project_id}/runs")
def list_project_runs(project_id: str):
    db = SessionLocal()
    try:
        jobs = db.query(Job).filter(Job.project_id == project_id).order_by(Job.created_at.desc()).all()
        return [
            {
                "task_id": job.task_id,
                "run_id": job.run_id,
                "job_type": job.job_type,
                "status": job.status,
                "created_at": job.created_at.isoformat()
            }
            for job in jobs
        ]
    finally:
        db.close()


@router.get("/{project_id}/results")
def get_project_results(
    project_id: str,
    run_id: str = Query(...),
    min_qed: float = Query(0.0),
    max_qed: float = Query(1.0),
    min_weight: float = Query(0.0),
    max_weight: float = Query(2000.0),
    min_logp: float = Query(-10.0),
    max_logp: float = Query(10.0),
    min_tpsa: float = Query(0.0),
    max_tpsa: float = Query(300.0),
    min_rotatable: int = Query(0),
    max_rotatable: int = Query(20),
    min_donors: int = Query(0),
    max_donors: int = Query(10),
    min_acceptors: int = Query(0),
    max_acceptors: int = Query(10),
    output_format: str = Query("csv", enum=["csv", "json"]),
    preview: bool = Query(False)
):
    import pandas as pd

    result_path = PROJECT_ROOT / project_id / "runs" / run_id / "results.csv"
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Results not found.")

    try:
        df = pd.read_csv(result_path)

        # Apply all filters
        if "QED" in df.columns:
            df = df[(df["QED"] >= min_qed) & (df["QED"] <= max_qed)]
        if "MolecularWeight" in df.columns:
            df = df[(df["MolecularWeight"] >= min_weight) & (df["MolecularWeight"] <= max_weight)]
        if "SlogP" in df.columns:
            df = df[(df["SlogP"] >= min_logp) & (df["SlogP"] <= max_logp)]
        if "TPSA" in df.columns:
            df = df[(df["TPSA"] >= min_tpsa) & (df["TPSA"] <= max_tpsa)]
        if "NumRotatableBonds" in df.columns:
            df = df[(df["NumRotatableBonds"] >= min_rotatable) & (df["NumRotatableBonds"] <= max_rotatable)]
        if "NumHDonors" in df.columns:
            df = df[(df["NumHDonors"] >= min_donors) & (df["NumHDonors"] <= max_donors)]
        if "NumHAcceptors" in df.columns:
            df = df[(df["NumHAcceptors"] >= min_acceptors) & (df["NumHAcceptors"] <= max_acceptors)]

        if preview:
            return JSONResponse(content=df.head(10).to_dict(orient="records"))

        if output_format == "json":
            return JSONResponse(content=df.to_dict(orient="records"))

        filtered_path = result_path.parent / f"filtered_results.csv"
        df.to_csv(filtered_path, index=False)
        return FileResponse(filtered_path, media_type="text/csv", filename=filtered_path.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering results: {str(e)}")
