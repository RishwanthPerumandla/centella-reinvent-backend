from celery import Celery
import subprocess
import os
from pathlib import Path
import uuid
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, QED
from src.db.connection import SessionLocal
from src.db.models import Job

# Setup Celery
celery_app = Celery(
    "generation",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.update(
    task_routes={"src.tasks.generation.run_sampling_from_agent": {"queue": "generation"}}
)

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))
DEVICE = os.environ.get("DEVICE", "cpu")

def compute_descriptors(smiles_list):
    results = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol:
            try:
                results.append({
                    "SMILES": smi,
                    "QED": QED.qed(mol),
                    "MolecularWeight": Descriptors.MolWt(mol),
                    "SlogP": Descriptors.MolLogP(mol),
                    "TPSA": Descriptors.TPSA(mol),
                    "NumRotatableBonds": Descriptors.NumRotatableBonds(mol),
                    "NumHDonors": Descriptors.NumHDonors(mol),
                    "NumHAcceptors": Descriptors.NumHAcceptors(mol)
                })
            except:
                continue
    return pd.DataFrame(results)

@celery_app.task(name="src.tasks.generation.run_sampling_from_agent", bind=True)
def run_sampling_from_agent(self,project_id: str):
    print(f"[TASK STARTED] Generating molecules for project {project_id}")

    run_id = f"run_{uuid.uuid4().hex}"
    run_path = PROJECT_ROOT / project_id / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)

    model_file = PROJECT_ROOT / project_id / "models/agent.pt"
    raw_output = run_path / "raw_results.csv"
    json_output = run_path / "sampling.json"
    config_path = run_path / "config.toml"
    log_path = run_path / "sample.log"

    toml_content = f"""
run_type = "sampling"
device = "{DEVICE}"
json_out_config = "{json_output}"

[parameters]
model_file = "{model_file}"
output_file = "{raw_output}"
num_smiles = 128
unique_molecules = true
randomize_smiles = true
"""

    try:
        with open(config_path, "w") as f:
            f.write(toml_content)
        print(f"[INFO] TOML config written at: {config_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write TOML: {e}")
        return

    # Log job to database
    try:
        db = SessionLocal()
        task_id = self.request.id  # ✅ correct way

        job = Job(task_id=task_id, project_id=project_id, run_id=run_id, job_type="generate")
        db.add(job)
        db.commit()
        db.close()
    except Exception as e:
        print(f"[ERROR] Failed to log job to DB: {e}")

    try:
        result = subprocess.run([
            "reinvent",
            "-l", str(log_path),
            str(config_path)
        ], capture_output=True, text=True)

        print("[STDOUT]", result.stdout)
        print("[STDERR]", result.stderr)

        if result.returncode != 0:
            raise RuntimeError(f"REINVENT failed: {result.stderr}")

    except Exception as e:
        print(f"[ERROR] REINVENT generation failed: {e}")
        return

    try:
        df = pd.read_csv(raw_output)
        df = compute_descriptors(df["SMILES"].tolist())
        scored_output = run_path / "results.csv"
        df.to_csv(scored_output, index=False)
        print(f"[INFO] Scored results saved to: {scored_output}")
    except Exception as e:
        error_log = run_path / "error.log"
        with open(error_log, "w") as err:
            err.write(str(e))
        print(f"[ERROR] Failed to compute descriptors: {e}")
