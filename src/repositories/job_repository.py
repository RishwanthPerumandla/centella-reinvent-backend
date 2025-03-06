from sqlalchemy.orm import Session
from src.db.models import Job

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, task_id: str, status: str):
        new_job = Job(task_id=task_id, status=status)
        self.db.add(new_job)
        self.db.commit()
        return new_job

    def update_job_status(self, task_id: str, status: str):
        job = self.db.query(Job).filter(Job.task_id == task_id).first()
        if job:
            job.status = status
            self.db.commit()
        return job

# Why?

# Encapsulates DB operations → Avoids redundant query logic
# Promotes separation of concerns
