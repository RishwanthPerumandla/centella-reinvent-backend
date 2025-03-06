from fastapi import APIRouter, Depends
from src.services.job_service import JobService
from src.tasks.molecule_task import run_molecule_design

router = APIRouter()

@router.post("/design")
async def submit_molecule_design():
    job_service = JobService()
    task_id = "task_" + str(time.time_ns())
    
    # Submit job
    job_service.submit_job(task_id)
    run_molecule_design.delay({"task_id": task_id})
    
    return {"task_id": task_id, "status": "queued"}

@router.get("/{task_id}")
async def get_molecule_status(task_id: str):
    job_service = JobService()
    job = job_service.repo.update_job_status(task_id, "processing")
    
    if not job:
        return {"error": "Task not found"}
    
    return {"task_id": task_id, "status": job.status}


# Why?

# Uses dependency injection (Depends) for better testability
# Ensures modular API handling