from src.repositories.job_repository import JobRepository
from src.db.connection import SessionLocal

class JobService:
    def __init__(self):
        self.db = SessionLocal()
        self.repo = JobRepository(self.db)

    def submit_job(self, task_id: str):
        return self.repo.create_job(task_id, status="queued")

    def update_status(self, task_id: str, status: str):
        return self.repo.update_job_status(task_id, status)


# Why?

# Separates business logic from API handlers
# Encapsulates job creation and updates
