### **REINVENT Backend Development Plan for FastAPI API**

Below is a detailed breakdown of what has been achieved so far and what remains to be done for building the backend API for the **REINVENT 4** molecular design tool.

---

## **Stage 1: Setup & Sampling (✅ Done)**
| **Step** | **Status** | **Details** |
|-----------|-------------|---------------|
| **Environment Setup** | ✅ Done | Python 3.10, Dependencies, and REINVENT installation completed. |
| **Sampling Configuration File (`config.toml`)** | ✅ Done | Configuration file created dynamically in `/app/reinvent/tasks/<task_id>/config.toml`. |
| **API Endpoint for Molecule Sampling** | ✅ Done | `/api/v1/molecule/design` endpoint created with FastAPI. |
| **Celery Task Integration** | ✅ Done | Celery worker successfully runs sampling logic. |
| **Sample Files Generation** | ✅ Done | `reinvent.log`, `sampling.json`, and `results.csv` successfully generated. |
| **Docker Integration for Running REINVENT** | ✅ Done | Runs REINVENT using Docker command: `docker exec reinvent_container reinvent -l reinvent.log config.toml`. |

✅ Sampling is complete and generates molecules based on the **prior model**.

---

## **Stage 2: Data Preparation (⏳ Partially Done)**
| **Step** | **Status** | **Details** |
|-----------|-------------|---------------|
| **Data Pipeline Configuration (`data_pipeline.toml`)** | ❗Not Implemented | Needs an API endpoint for data preparation. |
| **SMILES Splitting (Training/Test Data)** | ❗Not Implemented | Requires parsing SMILES and separating into training and test datasets. |
| **Data Pipeline Execution** | ❗Not Implemented | Should automate CSV file loading, SMILES filtering, and splitting logic. |

⏳ Partially complete — requires additional logic for SMILES filtering, dataset splitting, and storage.

---

## **Stage 3: Transfer Learning (TL) (❗ Not Started)**
| **Step** | **Status** | **Details** |
|-----------|-------------|---------------|
| **Transfer Learning Configuration (`transfer_learning.toml`)** | ❗Not Implemented | Requires endpoint for defining TL configurations. |
| **API Endpoint for Transfer Learning** | ❗Not Implemented | A new endpoint to accept TL parameters. |
| **Transfer Learning Execution** | ❗Not Implemented | Celery task logic to run TL needs to be created. |
| **Model Checkpoint Storage** | ❗Not Implemented | Needs logic to save TL model checkpoints every few epochs. |
| **Validation Integration** | ❗Not Implemented | Logic to evaluate TL model using validation data. |

🚨 Key Task: Extend Celery logic to trigger TL execution, manage outputs, and checkpoints.

---

## **Stage 4: Reinforcement Learning (RL) (❗ Not Started)**
| **Step** | **Status** | **Details** |
|-----------|-------------|---------------|
| **RL Configuration File (`staged_learning.toml`)** | ❗Not Implemented | Requires endpoint to define RL configurations. |
| **API Endpoint for Reinforcement Learning** | ❗Not Implemented | Needs new API endpoint for RL execution. |
| **RL Execution Logic in Celery** | ❗Not Implemented | Requires logic to initiate RL tasks in REINVENT. |
| **Output Generation for Stage 2 (Stage2_1.csv)** | ❗Not Implemented | Requires post-processing logic for saving RL results. |
| **Filtering and Visualization API** | ❗Not Implemented | Endpoint to filter molecules and generate visualizations like PCA/t-SNE. |

🚨 Key Task: Implement RL training logic with efficient checkpointing and scoring mechanism.

---

## **Stage 5: Results & Analysis (❗ Not Started)**
| **Step** | **Status** | **Details** |
|-----------|-------------|---------------|
| **Output Summary Generation** | ❗Not Implemented | Implement logic for creating `Stage2_1.csv`. |
| **Molecule Filtering** | ❗Not Implemented | Add options for QED/Chemprop-based filtering in the API. |
| **Visualization Integration** | ❗Not Implemented | Visual representation like PCA or t-SNE clustering. |

🚨 Final stage to ensure smooth analysis and presentation of generated molecules.

---

## **Summary of Progress**
✅ Sampling logic — Successfully implemented.  
⏳ Data preparation — Partially done; requires dataset splitting logic.  
❗ Transfer Learning — Requires endpoint, Celery task logic, and model checkpointing.  
❗ Reinforcement Learning — Requires detailed pipeline development.  
❗ Results & Analysis — Yet to be implemented.  

---

## **Recommended Next Steps**
1. **Implement Data Preparation Logic** (SMILES filtering, splitting, etc.).
2. **Add Transfer Learning API Endpoint** — Build Celery logic to run TL with dynamic configuration.
3. **Develop RL Pipeline** — Extend Celery logic for RL with improved scoring and filtering logic.
4. **Add Results API** — For downloading results, visualizing molecules, and evaluating scores.




TODO TODODODODOD


Yes, the workflow you have aligns with the **REINVENT** backend development plan. Below is how it maps with the REINVENT process:

### **Alignment Between Workflow & REINVENT Stages**
---
### **1. Setup Phase** ✅ (DONE)
- **Workflow Step:** User installs dependencies, sets up Python & Docker environments.
- **REINVENT Step:** 
  - Install dependencies (`pip install -r requirements-linux-64.lock`).
  - Install PyTorch.
  - Install REINVENT from source (`pip install --no-deps .`).
  - Set up environment (`conda create --name reinvent4 python=3.10`).

**✅ Status:** Already Done.

---
### **2. Initial TL-RL Learning (Stage 1)**
#### **A. Create/Reset Output Directory** ✅ (DONE)
- **Workflow Step:** User creates a directory for storing results.
- **REINVENT Step:** We already set up `/app/reinvent/tasks/{task_id}`.

**✅ Status:** Already Done.

#### **B. Define Parameters** ✅ (PARTIALLY DONE)
- **Workflow Step:** User defines model parameters (prior model, agent file, batch size, RL strategy).
- **REINVENT Step:** The `config.toml` is generated dynamically with:
  - `model_file`
  - `output_file`
  - `num_smiles`
  - `unique_molecules`
  - `randomize_smiles`

**✅ Status:** Done for Sampling, but needs expansion for TL-RL.

#### **C. Write Configuration File for TL** ❌ (NOT DONE)
- **Workflow Step:** Create `transfer_learning.toml`.
- **REINVENT Step:** This requires a proper transfer learning setup.

**❌ Status:** Not yet implemented.

#### **D. Retrieve Ligand SMILES & Split Data** ❌ (NOT DONE)
- **Workflow Step:** User retrieves molecule SMILES from ChEMBL/PDB and splits into train/test data.
- **REINVENT Step:** This involves processing input data.

**❌ Status:** Needs a new route to handle SMILES retrieval.

#### **E. Set Up TL Parameters** ❌ (NOT DONE)
- **Workflow Step:** Configure TL settings (CPU/GPU, epochs, batch size).
- **REINVENT Step:** Update configuration files dynamically.

**❌ Status:** Need a TL configuration route.

#### **F. Run TL and Generate Output** ❌ (NOT DONE)
- **Workflow Step:** User starts training.
- **REINVENT Step:** This would run `transfer_learning.toml` instead of `sampling.toml`.

**❌ Status:** Needs execution logic.

---
### **3. Reinforcement Learning (Stage 2)**
#### **A. Define Stage 2 Parameters** ❌ (NOT DONE)
- **Workflow Step:** User defines RL parameters.
- **REINVENT Step:** Requires `staged_learning.toml` config.

**❌ Status:** Needs configuration.

#### **B. Run RL** ❌ (NOT DONE)
- **Workflow Step:** Execute Reinforcement Learning.
- **REINVENT Step:** Call `reinvent` with RL config.

**❌ Status:** Not yet implemented.

#### **C. Save Output Summary to `Stage2_1.csv`** ❌ (NOT DONE)
- **Workflow Step:** Store RL results.
- **REINVENT Step:** Extract the final molecules.

**❌ Status:** Needs post-processing.

#### **D. Filter Molecules (QED & Chemprop Scores)** ❌ (NOT DONE)
- **Workflow Step:** Remove duplicates, filter low-quality molecules.
- **REINVENT Step:** Implement molecule filtering logic.

**❌ Status:** Needs additional processing.

#### **E. Visualize Molecules** ❌ (NOT DONE)
- **Workflow Step:** Generate molecule graphs, PCA/t-SNE clustering.
- **REINVENT Step:** Use RDKit visualization.

**❌ Status:** Needs visualization route.

---
### **Next Steps for Backend API**
Now that we've established what’s missing, the next **FastAPI routes** to implement:

| **Route** | **Description** | **Status** |
|-----------|----------------|------------|
| `POST /api/v1/molecule/design` | Submit molecule generation (sampling) ✅ | **Done** |
| `GET /api/v1/molecule/{task_id}/result` | Retrieve results ✅ | **Done** |
| `POST /api/v1/molecule/transfer_learning` | Start Transfer Learning ❌ | **Not Done** |
| `GET /api/v1/molecule/{task_id}/tl_status` | Get Transfer Learning progress ❌ | **Not Done** |
| `POST /api/v1/molecule/reinforcement_learning` | Start RL stage ❌ | **Not Done** |
| `GET /api/v1/molecule/{task_id}/rl_status` | Get RL progress ❌ | **Not Done** |
| `GET /api/v1/molecule/{task_id}/filter` | Filter molecules (QED, Chemprop) ❌ | **Not Done** |
| `GET /api/v1/molecule/{task_id}/visualize` | Visualize molecules ❌ | **Not Done** |

---
### **Final Summary**
✅ **Setup Phase is Completed.**  
✅ **Molecule sampling (Stage 1) is partially done.**  
❌ **Transfer Learning (Stage 1) is missing execution.**  
❌ **Reinforcement Learning (Stage 2) is not implemented.**  
❌ **Filtering, visualization, and clustering need to be implemented.**  

---
### **What You Need to Do Next**
1. **Implement TL stage**: Add routes to start transfer learning.
2. **Implement RL stage**: Allow reinforcement learning execution.
3. **Post-processing**: Filter molecules and provide visualizations.
4. **Error handling**: Ensure logs are properly stored and retrieved.