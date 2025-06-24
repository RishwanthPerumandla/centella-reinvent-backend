#  routes/project.py
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.responses import FileResponse
import os
import uuid
from pathlib import Path
from src.services.project_service import create_project_dir, save_smiles_file
from src.tasks.run_transfer_learning import run_transfer_learning_task
from src.tasks.run_reinforcement_learning import run_reinforcement_learning_task
from src.tasks.run_generation import run_sampling_from_agent

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
def train_model(project_id: str, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_transfer_learning_task, project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
    return {"project_id": project_id, "status": "training_started"}

@router.post("/{project_id}/reinforce")
def reinforce_model(project_id: str, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_reinforcement_learning_task, project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reinforcement learning failed: {str(e)}")
    return {"project_id": project_id, "status": "reinforcement_started"}

@router.post("/{project_id}/generate")
def generate_molecules(project_id: str, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_sampling_from_agent, project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
    return {"project_id": project_id, "status": "generation_started"}

@router.get("/{project_id}/results")
def get_project_results(
    project_id: str,
    run_id: str = Query(...),
    min_qed: float = Query(0.0),
    max_qed: float = Query(1.0),
    min_weight: float = Query(0.0),
    max_weight: float = Query(2000.0),
    min_logp: float = Query(-10.0),
    max_logp: float = Query(10.0)
):
    import pandas as pd

    result_path = PROJECT_ROOT / project_id / "runs" / run_id / "results.csv"
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Results not found.")

    try:
        df = pd.read_csv(result_path)
        if "QED" in df.columns:
            df = df[(df["QED"] >= min_qed) & (df["QED"] <= max_qed)]
        if "MolecularWeight" in df.columns:
            df = df[(df["MolecularWeight"] >= min_weight) & (df["MolecularWeight"] <= max_weight)]
        if "SlogP" in df.columns:
            df = df[(df["SlogP"] >= min_logp) & (df["SlogP"] <= max_logp)]

        filtered_path = result_path.parent / f"filtered_{min_qed}_{max_qed}_{min_weight}_{max_weight}_{min_logp}_{max_logp}.csv"
        df.to_csv(filtered_path, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering results: {str(e)}")

    return FileResponse(filtered_path, media_type="text/csv", filename=filtered_path.name)
