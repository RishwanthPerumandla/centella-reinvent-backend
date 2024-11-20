# Centella Reinvent Backend

Centella Reinvent Backend provides the infrastructure to support **REINVENT 4**, a molecular design tool for de novo design, scaffold hopping, R-group replacement, linker design, molecule optimization, and more. The backend is designed for high scalability, fault tolerance, and efficient interaction with REINVENT's Reinforcement Learning (RL) and Transfer Learning (TL) models.

---

## Overview

This project aims to deliver a robust backend to handle tasks such as molecule design, job management, and file storage while ensuring scalability and fault tolerance.

---

## Project Features

### Core Features
- **User Authentication**:
  - Secure login/signup functionality.
  - Token-based authentication (e.g., JWT or OAuth2).
- **Molecule Design Tasks**:
  - APIs to interact with REINVENT functionalities like de novo design and scaffold hopping.
  - Handle model inputs (e.g., chemical structures, score functions).
- **Model Handling**:
  - Load and manage pre-trained models for Transfer Learning (TL).
  - Enable saving/loading of user-specific models or results.
- **Job Management**:
  - Asynchronous handling for lengthy molecular design tasks using Celery.
- **Result Management**:
  - Save generated molecules and metadata to a database.
  - Allow users to retrieve past results.
- **File Management**:
  - Support for uploading and downloading datasets and molecule files.

---

## Tech Stack

| **Component**          | **Technology**         | **Purpose**                                |
|-------------------------|------------------------|--------------------------------------------|
| Backend Framework       | FastAPI               | API development and request handling.      |
| Asynchronous Tasks      | Celery + Redis        | Job queue for handling long-running tasks. |
| Database                | PostgreSQL            | Store user data, molecules, and results.   |
| File Storage            | AWS S3 / Local FS     | Store datasets and generated molecules.    |
| Authentication          | OAuth2 / JWT          | Secure access to the APIs.                 |
| Model Serving           | Python (custom handler) | Load and run REINVENT models.            |
| Containerization        | Docker                | Consistent environments and deployment.    |

---

## Project Milestones

### Phase 1 - Project Initialization
1. Set up FastAPI project structure.
2. Initialize Docker containers for:
   - Backend application.
   - Model environment.
3. Set up PostgreSQL database for user and result management.
4. Integrate Redis for job queuing.

### Phase 2 - Core Features
1. Implement user authentication (login/signup, JWT).
2. Develop APIs to load and interact with REINVENT models:
   - Model selection.
   - Score function input and validation.
3. Add file upload/download functionality.

### Phase 3 - Advanced Features
1. Enable Transfer Learning:
   - APIs for uploading datasets.
   - APIs to train models with user data.
2. Develop job management APIs:
   - Submit tasks.
   - Poll for task status.
   - Retrieve task results.
3. Optimize database for scalability and queries.

### Phase 4 - Deployment and Scaling
1. Deploy to Azure using Docker containers.
2. Enable logging and monitoring with Prometheus and Grafana.
3. Implement auto-scaling for model-heavy workloads.

---

<!-- ## Installation

### Prerequisites
- Python 3.9 or higher.
- Docker and Docker Compose.
- PostgreSQL and Redis installed locally or accessible through cloud services. -->


<!-- Pending yet -->
## **Documentation**
Detailed project information is available in the /docs folder:

 [Setup Instructions](docs/setup_instructions.md)
 