from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    task_id = Column(String, primary_key=True, index=True)
    status = Column(Enum("queued", "processing", "completed", "failed", name="status_enum"), default="queued")

# Why?

# Encapsulates DB models separately
# Uses SQLAlchemy ORM for better maintainability