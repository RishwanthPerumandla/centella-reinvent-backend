# **Centella Reinvent Backend – Setup & Deployment Guide**

## **Project Overview**
This project integrates **FastAPI**, **Celery**, and **Docker** to run **REINVENT** as a molecular design pipeline. The setup allows users to submit molecule design tasks, process them asynchronously via Celery workers, and execute them inside Docker containers.

---

## **1. Setup & Installation**
### **1.1 Clone the Backend Repository**
```sh
git clone <repo-url> //edit
cd <backend-repo> //edit
```

### **1.2 Clone the REINVENT Repository**
Since REINVENT is large (~1.7GB), **do this manually** inside the backend repo:
```sh
git clone https://github.com/MolecularAI/REINVENT4.git reinvent
```
Ensure that `reinvent` is **not cloned again** during Docker builds.

### **1.3 Add Environment Variables**
Create a `.env` file in the root directory:
```sh
# PostgreSQL Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=reinventdb

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Celery Configuration
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

---

## **2. Running the Application**
### **2.1 Start Docker Services**
```sh
 docker build -f Dockerfile.reinvent -t reinvent:latest .
docker-compose up --build -d
```
This will:
- Start **PostgreSQL** (`db`)
- Start **Redis** (`redis`)
- Start **FastAPI Backend** (`backend`)
- Start **Celery Worker** (`celery_worker`)
- Start **REINVENT** (`reinvent`)

### **2.2 Verify Running Containers**
Check running containers:
```sh
docker ps
```
If `reinvent` isn't running, it will start dynamically when a request is made.

---

## **3. Project Structure**
```
/backend-repo
│── reinvent/  # REINVENT codebase (cloned)
│── reinvent/tasks/  # Each molecule task has its own folder
│── reinvent/configs/  # Generated TOML config files
│── reinvent/results/  # Output JSONs
│── reinvent/logs/  # Logs from each execution
│── src/
│   ├── api/  # FastAPI routes
│   ├── tasks/  # Celery task management
│   ├── db/  # Database connection
│── docker-compose.yml  # Docker setup
│── Dockerfile  # Backend FastAPI Dockerfile
│── Dockerfile.reinvent  # REINVENT Dockerfile
│── .env  # Environment variables
```

---

## **4. API Endpoints**
### **4.1 Submit a Molecule Design Task**
```http
POST /api/v1/molecule/design
```
#### **Request Body**
```json
{
    "device": "cpu",
    "model_file": "priors/reinvent.prior",
    "num_smiles": 157,
    "unique_molecules": true,
    "randomize_smiles": true
}
```
#### **Response**
```json
{
    "task_id": "task_xxxxxxx",
    "celery_task_id": "celery-xxxxx",
    "status": "queued"
}
```

---

### **4.2 Get Molecule Design Results**
```http
GET /api/v1/molecule/result/{task_id}
```
#### **Response (Success)**
```json
{
    "task_id": "task_xxxxx",
    "status": "completed",
    "result": "<CSV or JSON output>"
}
```
#### **Response (Failure)**
```json
{
    "task_id": "task_xxxxx",
    "status": "failed",
    "error": "File not found"
}
```

---

## **5. Running Celery Manually**
To monitor **Celery tasks**, open a terminal inside the backend container:
```sh
docker exec -it <backend-container-id> sh
```
Run:
```sh
celery -A src.tasks.molecule_task worker --loglevel=debug
```

Check active tasks:
```sh
celery -A src.tasks.molecule_task inspect active
```

---

## **6. Debugging & Common Issues**
### **6.1 No Such Container: reinvent**
- **Solution:** Ensure the REINVENT container name is **dynamically fetched**.
```sh
docker ps --filter "name=reinvent"
```
If no output, run:
```sh
docker-compose up --build -d
```

### **6.2 Celery Not Processing Tasks**
Check Redis is running:
```sh
redis-cli ping
```
If `PONG` is not received, restart Redis:
```sh
docker-compose restart redis
```

Check Celery queues:
```sh
celery -A src.tasks.molecule_task inspect active_queues
```

---

## **7. Automating Deployment**
To make updates:
```sh
git pull origin main
docker-compose down
docker-compose up --build -d
```

---

## **Final Notes**
- **Molecule design tasks run inside Docker containers dynamically.**
- **All logs, configs, and results are stored inside `reinvent/tasks/{task_id}/` for clarity.**
- **Ensure Celery workers and Redis are active before submitting requests.**


## **📌 Todo**
- ✅ Improve API logging for better debugging.
- ✅ Add a front-end dashboard for tracking task progress.
- ✅ Introduce persistent storage for task results.

