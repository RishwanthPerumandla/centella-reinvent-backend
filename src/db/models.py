from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    task_id = Column(String, primary_key=True, index=True)
    status = Column(String, default="queued")
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    task_id = Column(String, primary_key=True, index=True)
    status = Column(String, default="queued")
