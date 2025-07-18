from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    task_id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=False)
    run_id = Column(String, nullable=False)
    job_type = Column(String, nullable=False)  # train / reinforce / generate
    status = Column(String, default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)
