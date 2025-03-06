# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/

# Expose port
EXPOSE 8000

# Ensure environment variables are read inside the container
ENV DATABASE_URL=${DATABASE_URL}
ENV PYTHONPATH=/app

# Run FastAPI
# Run database initialization script before starting the app
CMD ["sh", "-c", "python src/db/init_db.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
