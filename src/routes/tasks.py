import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult
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

@router.post("/submit")
async def submit_task(job_service: JobService = Depends(get_job_service)):
    """ Submits a new task to Celery and stores its metadata in the database. """

    task_id = f"task_{uuid.uuid4().hex}"  # Unique task identifier
    logger.info(f"Submitting new task: {task_id}")

    try:
        # Store task in DB
        job_service.submit_job(task_id)

        # Submit Celery task
        task_result = run_molecule_design.delay({"task_id": task_id})
    except Exception as e:
        logger.error(f"Task submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Task submission failed")

    return {"task_id": task_id, "celery_task_id": task_result.id, "status": "queued"}

@router.get("/{task_id}")
async def get_task_status(task_id: str, job_service: JobService = Depends(get_job_service)):
    """ Retrieves the status of a submitted task from Celery & database. """

    job = job_service.get_job_by_id(task_id)

    if not job:
        logger.warning(f"Task ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    # Fetch Celery task status
    celery_result = AsyncResult(job.task_id)
    task_status = celery_result.status

    return {"task_id": task_id, "status": job.status, "celery_status": task_status}

@router.get("/{task_id}/result")
async def get_task_result(task_id: str, job_service: JobService = Depends(get_job_service)):
    """ Retrieves the result of a completed task if available. """

    job = job_service.get_job_by_id(task_id)
    
    if not job:
        logger.warning(f"Task ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    # Fetch Celery task result
    celery_result = AsyncResult(job.task_id)
    if not celery_result.ready():
        return {"task_id": task_id, "status": job.status, "message": "Result not available yet"}

    return {"task_id": task_id, "status": "completed", "result": celery_result.result}
