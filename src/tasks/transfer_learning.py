from celery import Celery
import subprocess
import os
from pathlib import Path
import uuid
from src.db.connection import SessionLocal
from src.db.models import Job

# Setup Celery
celery_app = Celery(
    "transfer_learning",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.update(
    task_routes={"src.tasks.transfer_learning.run_transfer_learning_task": {"queue": "tl"}}
)

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))
DEVICE = os.environ.get("DEVICE", "cpu")  # <-- Dynamic device toggle

@celery_app.task(name="src.tasks.transfer_learning.run_transfer_learning_task",bind=True)
def run_transfer_learning_task(self,project_id: str):
    print(f"[TASK STARTED] Training project {project_id}")

    project_path = PROJECT_ROOT / project_id
    input_path = project_path / "input"
    model_path = project_path / "models"
    config_path = project_path / "config.toml"

    model_in = "reinvent/priors/reinvent.prior"
    model_out = model_path / "agent.pt"
    train_file = input_path / "train.csv"

    # Ensure necessary directories exist
    input_path.mkdir(parents=True, exist_ok=True)
    model_path.mkdir(parents=True, exist_ok=True)

    # Build TOML content
    toml_content = f"""
run_type = "transfer_learning"
device = "{DEVICE}"

[parameters]
input_model_file = "{model_in}"
output_model_file = "{model_out}"
smiles_file = "{train_file}"
num_epochs = 10
batch_size = 128
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

        job = Job(task_id=task_id, project_id=project_id, run_id="N/A", job_type="train", status="queued")
        db.add(job)
        db.commit()
        db.close()
        print(f"[INFO] Job logged to DB with task_id: {task_id}")

    except Exception as e:
        print(f"[ERROR] Failed to log job to DB: {e}")

    # Run REINVENT
    try:
        result = subprocess.run([
            "reinvent",
            "-l", str(project_path / "train.log"),
            str(config_path)
        ], capture_output=True, text=True)

        print("[STDOUT]", result.stdout)
        print("[STDERR]", result.stderr)

        if result.returncode != 0:
            raise RuntimeError(f"REINVENT failed: {result.stderr}")

    except Exception as e:
        print(f"[ERROR] REINVENT training failed: {e}")
        raise
