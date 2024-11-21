from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Use the DATABASE_URL from environment variables or default to SQLite
DATABASE_URL = settings.database_url  # e.g., "postgresql://user:password@localhost/reinvent"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
