**Backend Development Plan for REINVENT API**

## **Overview**
The goal is to build a backend API that integrates with the open-source REINVENT repository to support molecular design through Transfer Learning (TL) and Reinforcement Learning (RL). The backend will handle task submission, configuration management, execution, result retrieval, and visualization.

---

## **Stage-Wise Breakdown**

### **Stage 0: Setup & Infrastructure**  
**Tasks Done:**
- Dockerized REINVENT backend with FastAPI and Celery workers
- Integrated Redis and PostgreSQL for task and job management
- API routes for task submission and result retrieval

**Pending Tasks:**
- Fix module dependencies (`iSIM` missing issue)
- Validate REINVENT installation and execution
- Automate environment setup (Dockerfile improvements)

---

### **Stage 1: Initial TL-RL Learning (Training Setup & Configuration)**

#### **Task 1: Create/Reset Output Directory**
**Tasks Done:**
- Created `/app/reinvent/tasks/{task_id}` for per-task storage

**Pending Tasks:**
- Ensure proper directory permissions for execution
- Handle cleanup of old task folders

#### **Task 2: Define Parameters**
**Tasks Done:**
- API accepts model file, number of SMILES, and scoring parameters

**Pending Tasks:**
- Add more configurable parameters (batch size, RL strategy, etc.)
- Validate input parameters before execution

#### **Task 3: Write Configuration File for TL**
**Tasks Done:**
- Generates `config.toml` for REINVENT execution

**Pending Tasks:**
- Improve error handling when writing configuration files
- Extend configuration generation for full TL setup

#### **Task 4: Retrieve Ligand SMILES**
**Pending Tasks:**
- Implement ChEMBL API integration for fetching ligand SMILES
- Store retrieved SMILES in the task directory

#### **Task 5: Split SMILES into Training and Test Data**
**Pending Tasks:**
- Implement SMILES dataset partitioning logic
- Store training and test data properly

#### **Task 6: Set Up TL Parameters**
**Pending Tasks:**
- Add TL-specific configurations (epochs, batch size, etc.)

#### **Task 7: Run TL and Create Output Model Files**
**Tasks Done:**
- Dockerized execution of REINVENT

**Pending Tasks:**
- Fix execution errors (iSIM module issue)
- Ensure model files are saved correctly
- Store logs for debugging

---

### **Stage 2: Reinforcement Learning (RL Execution & Optimization)**

#### **Task 1: Define Stage 2 Parameters**
**Pending Tasks:**
- Allow configuration of RL-specific parameters

#### **Task 2: Run RL**
**Pending Tasks:**
- Execute RL model training based on TL output
- Verify RL execution logs and error handling

#### **Task 3: Save Output Summary**
**Pending Tasks:**
- Ensure output files (`Stage2_1.csv`) are correctly stored
- Implement error handling for missing outputs

#### **Task 4: Filter Molecules**
**Pending Tasks:**
- Implement filtering logic based on QED and Chemprop scores
- Store filtered results in task directory

#### **Task 5: Visualize Molecules**
**Pending Tasks:**
- Implement molecule visualization (PCA, t-SNE clustering)
- Serve visualizations via API for frontend integration

---

### **Final Deliverables & API Endpoints**

#### **Existing API Endpoints:**
- `POST /api/v1/molecule/design` - Submits a molecule design task
- `GET /api/v1/molecule/{task_id}/result` - Retrieves task results

#### **New API Endpoints to Implement:**
- `GET /api/v1/molecule/{task_id}/logs` - Fetches logs for a task
- `GET /api/v1/molecule/{task_id}/visualization` - Returns molecule visualizations
- `GET /api/v1/molecule/{task_id}/filtered_results` - Returns filtered molecules
- `POST /api/v1/molecule/train` - Triggers TL training process
- `POST /api/v1/molecule/reinforce` - Triggers RL execution

---

## **Next Steps & Priorities**
1. **Fix Dependency Issues** - Resolve missing `iSIM` module issue.
2. **Enhance Configuration Management** - Support all TL and RL parameters.
3. **Improve Data Handling** - Fetch and store ligand SMILES.
4. **Validate Execution** - Ensure REINVENT runs without errors.
5. **Implement Filtering & Visualization** - Develop analysis & visualization endpoints.
6. **Optimize API Performance** - Enhance logging, error handling, and task tracking.

---

**Final Goal:** A fully operational backend that automates molecular design using REINVENT and provides API access to run, monitor, and visualize molecular generation results.

