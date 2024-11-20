# Setup Instructions for Centella Reinvent Backend

This guide walks you through setting up the Centella Reinvent Backend development environment. Follow the steps to ensure the project runs smoothly and consistently across different machines.

---

## **1. Prerequisites**

Ensure the following tools are installed on your machine:
- **Docker**: [Download and install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Included with most Docker installations ([Install Guide](https://docs.docker.com/compose/install/))
- **Git**: [Download and install Git](https://git-scm.com/downloads)

Optional for local development without Docker:
- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Comes pre-installed with Python 3.9+.

---

## **2. Clone the Repository**

Clone the project repository from GitHub to your local machine:
```bash
git clone https://github.com/RishwanthPerumandla/Centella-Reinvent-Backend.git
cd Centella-Reinvent-Backend
```

---

## **3. Running the Project Using Docker**

Docker is the recommended way to run the project as it ensures consistency across environments.

### **Step 1: Build Docker Containers**
Build the Docker containers for the backend, PostgreSQL, and Redis:
```bash
docker-compose build
```

### **Step 2: Start the Containers**
Start the containers using Docker Compose:
```bash
docker-compose up
```

The backend will now be accessible at:
- **API Base URL**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### **Step 3: Stop the Containers**
To stop the containers, press `Ctrl+C` or use:
```bash
docker-compose down
```

---

## **4. Running Locally Without Docker (Optional)**

If you prefer running the project locally without Docker, follow these steps:

### **Step 1: Set Up a Virtual Environment**
Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### **Step 2: Install Dependencies**
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### **Step 3: Run the Backend**
Start the FastAPI server locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be accessible at:
- **API Base URL**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## **5. Adding New Dependencies**

When you need to install new libraries, follow these steps to ensure consistency:

### **Step 1: Add to `requirements.txt`**
Add the library name to `requirements.txt`. For example:
```
requests
```

### **Step 2: Rebuild Docker Containers**
Rebuild the containers to include the new dependency:
```bash
docker-compose down
docker-compose up --build
```

### **Step 3: Verify Changes**
Test the application to confirm the new library is installed.

---

## **6. Common Issues and Fixes**

### **1. Changes Not Reflecting**
Ensure you’ve mounted the project directory as a volume in `docker-compose.yml`:
```yaml
volumes:
  - .:/app
```
Enable hot reloading by using the `--reload` flag in the `CMD` of the `Dockerfile`.

### **2. Port Conflicts**
If port `8000` is already in use, change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"
```

### **3. Database Connection Issues**
Ensure PostgreSQL is running in Docker and the credentials in `docker-compose.yml` match the application configuration.

---

## **7. Development Workflow**

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/Centella-Reinvent-Backend.git
   cd Centella-Reinvent-Backend
   ```

2. Start the containers:
   ```bash
   docker-compose up
   ```

3. Make changes to the code. Hot reloading will automatically apply changes in the running container.

4. Stop the containers when finished:
   ```bash
   docker-compose down
   ```

---

For further assistance, contact the maintainers or refer to the project's main documentation.
```

---