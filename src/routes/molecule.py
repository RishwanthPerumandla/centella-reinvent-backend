import uuid
import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.services.job_service import JobService
from src.tasks.molecule_task import run_molecule_design
from src.db.connection import SessionLocal

router = APIRouter()
logger = logging.getLogger(__name__)


# ✅ Dependency function to provide JobService instance
def get_job_service():
    db: Session = SessionLocal()
    try:
        yield JobService(db)
    finally:
        db.close()


# ✅ Pydantic Model for API Input Validation
class MoleculeDesignRequest(BaseModel):
    device: str = "cpu"
    model_file: str = "priors/reinvent.prior"
    num_smiles: int = 157
    unique_molecules: bool = True
    randomize_smiles: bool = True


@router.post("/design")
async def submit_molecule_design(
    request: MoleculeDesignRequest, job_service: JobService = Depends(get_job_service)
):
    """ Submits a molecule design task for processing. """

    task_id = f"task_{uuid.uuid4().hex}"
    logger.info(f"Submitting new molecule design task: {task_id}")

    try:
        # Store task in DB
        job_service.submit_job(task_id)

        # Submit Celery task with parameters
        task_data = request.dict()
        task_data["task_id"] = task_id
        task_result = run_molecule_design.delay(task_data)

    except Exception as e:
        logger.error(f"Failed to submit molecule design task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Task submission failed")

    return {"task_id": task_id, "celery_task_id": task_result.id, "status": "queued"}



@router.get("/{task_id}/result")
async def get_molecule_result(task_id: str, job_service: JobService = Depends(get_job_service)):
    """ Retrieves the result of a molecule design task if available. """

    result_path = f"./reinvent/results/{task_id}.csv"

    if not os.path.exists(result_path):
        raise HTTPException(status_code=404, detail="Result not found")

    with open(result_path, "r") as file:
        result_data = file.read()

    return {"task_id": task_id, "status": "completed", "result": result_data}
