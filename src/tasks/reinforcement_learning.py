from celery import Celery
import subprocess
import os
from pathlib import Path
import uuid
from src.db.connection import SessionLocal
from src.db.models import Job

# Setup Celery
celery_app = Celery(
    "reinforcement_learning",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.update(
    task_routes={"src.tasks.reinforcement_learning.run_reinforcement_learning_task": {"queue": "rl"}}
)

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))

@celery_app.task(name="src.tasks.reinforcement_learning.run_reinforcement_learning_task", bind=True)
def run_reinforcement_learning_task(self, project_id: str):
    print(f"[TASK STARTED] Reinforcing project {project_id}")

    run_id = f"run_{uuid.uuid4().hex}"
    run_path = PROJECT_ROOT / project_id / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)

    agent_model = PROJECT_ROOT / project_id / "models/agent.pt"
    prior_model = "reinvent/priors/reinvent.prior"
    output_csv = run_path / "results.csv"
    json_output = run_path / "sampling.json"
    config_path = run_path / "config.toml"
    log_path = run_path / "reinforce.log"

    toml_content = f"""
run_type = "sampling"
device = "cpu"
json_out_config = "{json_output}"

[parameters]
model_file = "{agent_model}"
output_file = "{output_csv}"
num_smiles = 256
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
        job = Job(task_id=task_id, project_id=project_id, run_id=run_id, job_type="reinforce")
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
        print(f"[ERROR] REINVENT reinforcement failed: {e}")
        raise
