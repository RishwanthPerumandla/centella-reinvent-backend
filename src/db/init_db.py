from src.db.connection import engine
from src.db.models import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
