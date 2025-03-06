from celery import Celery
import time
from src.services.job_service import JobService

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task(bind=True, retry_backoff=True, retry_kwargs={"max_retries": 3})
def run_molecule_design(self, params):
    job_service = JobService()
    task_id = params.get("task_id")

    try:
        job_service.update_status(task_id, "processing")
        time.sleep(10)  # Simulate molecular design task
        job_service.update_status(task_id, "completed")
        return {"task_id": task_id, "status": "completed"}
    except Exception as e:
        self.retry(exc=e)


# Why?

# Implements retry logic (max_retries=3) for handling transient failures
# Updates job status dynamically in DB