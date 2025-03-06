import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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

@router.post("/design")
async def submit_molecule_design(job_service: JobService = Depends(get_job_service)):
    """ Submits a molecule design task for processing. """
    
    task_id = f"task_{uuid.uuid4().hex}"
    logger.info(f"Submitting new molecule design task: {task_id}")

    try:
        # Store task in DB
        job_service.submit_job(task_id)
        
        # Submit Celery task
        run_molecule_design.delay({"task_id": task_id})
    except Exception as e:
        logger.error(f"Failed to submit molecule design task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Task submission failed")

    return {"task_id": task_id, "status": "queued"}

@router.get("/{task_id}")
async def get_molecule_status(task_id: str, job_service: JobService = Depends(get_job_service)):
    """ Retrieves the status of a molecule design task. """
    
    job = job_service.get_job_by_id(task_id)  # Fetch job

    if not job:
        logger.warning(f"Task ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task_id": task_id, "status": job.status}
