**Project: Backend API for REINVENT Molecular Design**

## **What Are We Doing?**
We are building a **backend API** to integrate and manage the **MolecularAI/REINVENT** open-source software, enabling users to perform **de novo molecular design** using **Reinforcement Learning (RL) and Transfer Learning (TL)**. The API will allow users to submit tasks, process molecular design requests, and retrieve results efficiently using **FastAPI, Celery, Redis, and Docker**.

---

## **What Is REINVENT?**
REINVENT is an AI-based molecular design tool that:
- Uses **Reinforcement Learning (RL)** to optimize molecules based on custom-defined scoring functions.
- Uses **Transfer Learning (TL)** to fine-tune a molecular generation model to generate structures similar to known molecules.
- Generates and optimizes molecules for **drug discovery, scaffold hopping, linker design, and molecular optimization**.

---

## **What Are We Building the Backend API For?**
We are building a **FastAPI-based backend** that:
1. **Manages the execution of molecular design tasks**: Users can submit requests, and tasks are executed asynchronously using **Celery** workers.
2. **Runs REINVENT inside a Docker container**: The API ensures that REINVENT is correctly configured and executed within a managed environment.
3. **Handles task execution via Celery**: REINVENT runs asynchronously, and results are stored in designated task directories.
4. **Processes and retrieves molecular results**: Users can fetch results from molecular design tasks once completed.
5. **Implements a structured workflow**: The API ensures **task management, parameter handling, and model execution** follows a structured, repeatable process.

---

## **How Does the Backend API Work?**
1. **User submits a molecular design task via API** (FastAPI)
2. **The request is queued for processing using Celery** (Task Management)
3. **The API executes REINVENT inside a Docker container** with task-specific configurations.
4. **REINVENT generates molecules based on defined parameters**.
5. **Results are saved in a structured output directory** (`tasks/{task_id}/results.csv`).
6. **Users retrieve results via API**.

---

## **What Have We Done So Far?**
✅ **FastAPI API for Submitting & Fetching Tasks**  
✅ **Task Execution with Celery & Redis**  
✅ **Dockerized Execution of REINVENT**  
✅ **Configuration File Generation for REINVENT**  
✅ **Basic Molecule Sampling & Generation Pipeline**  

---

## **What Still Needs to Be Done?**
🔲 **Implement Transfer Learning (TL) Workflow**  
🔲 **Implement Reinforcement Learning (RL) Workflow**  
🔲 **Store & Retrieve Molecular Design Results Efficiently**  
🔲 **Enhance API to Support More REINVENT Functionalities**  
🔲 **Ensure Scalability & Robust Error Handling**  

---

## **Final Goal:**
Deliver a **fully functional backend API** that enables users to run molecular design workflows (TL + RL), manage tasks, retrieve results, and scale efficiently for research and drug discovery.

