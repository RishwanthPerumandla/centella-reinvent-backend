# Centella Reinvent Backend - FastAPI & Celery

## Overview
This project is a backend API service for molecule design tasks, built with **FastAPI**, **Celery**, **PostgreSQL**, and **Redis**. It supports:

- **Task submission and tracking**
- **Database storage using PostgreSQL**
- **Asynchronous task processing using Celery & Redis**

## Project Structure
```
/app
│── src/
│   ├── db/
│   │   ├── models.py
│   │   ├── connection.py
│   │   ├── init_db.py
│   ├── services/
│   │   ├── job_service.py
│   ├── tasks/
│   │   ├── molecule_task.py
│   │   ├── celery_app.py
│   ├── routes/
│   │   ├── tasks.py
│   │   ├── molecule.py
│   ├── config/
│   │   ├── settings.py
│   ├── main.py
│── Dockerfile
│── Dockerfile.celery
│── docker-compose.yml
│── requirements.txt
│── .env
```

## Prerequisites
Ensure you have the following installed:
- **Docker & Docker Compose**
- **Python 3.10+** (for local development)

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/centella-reinvent-backend.git
cd centella-reinvent-backend
```

### 2️⃣ Setup Environment Variables
Create a `.env` file in the root directory and add:
```env
DATABASE_URL=postgresql://user:password@db/reinventdb
REDIS_URL=redis://redis:6379/0
```

### 3️⃣ Start Docker Containers
```bash
docker-compose up --build
```

This will start the following services:
- **Backend (FastAPI) →** `http://localhost:8000`
- **Database (PostgreSQL) →** `db` service
- **Task Queue (Celery) →** `celery_worker`
- **Message Broker (Redis) →** `redis`

### 4️⃣ Initialize Database
Run database migrations inside the running container:
```bash
docker exec -it backend-1 python /app/src/db/init_db.py
```
This will create the required tables inside **PostgreSQL**.

## API Endpoints

### **Task Management**
| Method | Endpoint | Description |
|--------|----------|--------------|
| `POST` | `/api/v1/tasks/submit` | Submits a new molecule design task |
| `GET` | `/api/v1/tasks/{task_id}` | Fetches the status of a submitted task |

### **Example Usage**

#### ✅ Submit a New Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/submit"
```

#### ✅ Check Task Status
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/task_id_here"
```

## Celery Worker Logs
To monitor Celery workers processing tasks, run:
```bash
docker logs -f celery_worker-1
```

## Troubleshooting

### ❌ Database Connection Error
If you see an error like:
```
psycopg2.OperationalError: connection to server at "db" failed
```
Make sure PostgreSQL is running by checking logs:
```bash
docker-compose logs db
```

### ❌ Module Not Found (e.g., `ModuleNotFoundError: No module named 'src'`)
Ensure the correct working directory inside the container:
```bash
docker exec -it backend-1 /bin/sh
cd /app/src && ls
```

## Next Steps
- **Implement additional API routes for molecule processing**
- **Enhance error handling and logging**
- **Write unit tests using Pytest**

---

**Contributors:**
- **@RishwanthPerumandla** - Backend & Celery Integration
- **@RishwanthPerumandla** - API Routes Development

