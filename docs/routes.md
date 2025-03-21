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
