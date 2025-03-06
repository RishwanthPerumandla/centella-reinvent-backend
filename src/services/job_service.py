from sqlalchemy.orm import Session
from src.db.models import Job  # Ensure Job model is correctly imported

class JobService:
    def __init__(self, db: Session):
        self.db = db

    def submit_job(self, task_id: str):
        """ Inserts a new job into the database. """
        new_job = Job(task_id=task_id, status="queued")
        self.db.add(new_job)
        self.db.commit()
        self.db.refresh(new_job)

    def get_job_by_id(self, task_id: str):
        """ Fetches a job record by its task_id. """
        return self.db.query(Job).filter(Job.task_id == task_id).first()

    def update_job_status(self, task_id: str, status: str):
        """ Updates the status of a job in the database. """
        job = self.get_job_by_id(task_id)
        if job:
            job.status = status
            self.db.commit()
            return job
        return None
