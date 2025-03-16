import os
import subprocess
import uuid
from celery import Celery

celery_app = Celery(
    "molecule_task",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_routes={"src.tasks.molecule_task.run_molecule_design": {"queue": "molecule"}}
)

@celery_app.task(name="src.tasks.molecule_task.run_molecule_design")
def run_molecule_design(task_data: dict):
    """Runs the molecule design pipeline using REINVENT inside a managed folder"""

    task_id = task_data.get("task_id", f"task_{uuid.uuid4().hex}")
    device = task_data.get("device", "cpu")
    model_file = task_data.get("model_file", "priors/reinvent.prior")
    num_smiles = task_data.get("num_smiles", 157)
    unique_molecules = task_data.get("unique_molecules", True)
    randomize_smiles = task_data.get("randomize_smiles", True)

    print(f"[DEBUG] Task ID: {task_id}")

    # Define task-specific folder
    task_folder = f"/app/reinvent/tasks/{task_id}"
    os.makedirs(task_folder, exist_ok=True)

    # Define paths inside the task-specific folder
    reinvent_config_path = f"{task_folder}/config.toml"
    log_path = f"{task_folder}/reinvent.log"
    json_out_path = f"{task_folder}/sampling.json"  # ✅ Ensure _sampling.json goes in tasks folder
    result_path = f"{task_folder}/results.csv"  # ✅ Ensure results CSV stays in task folder

    print(f"[DEBUG] Writing config file to: {reinvent_config_path}")

    # Create a TOML config file dynamically
    toml_content = f"""
run_type = "sampling"
device = "{device}"
json_out_config = "{json_out_path}"  # ✅ Ensures _sampling.json is inside task folder

[parameters]
model_file = "{model_file}"
output_file = "{result_path}"  # ✅ Ensures results.csv is saved in the task folder

num_smiles = {num_smiles}
unique_molecules = {str(unique_molecules).lower()}
randomize_smiles = {str(randomize_smiles).lower()}
"""

    # Ensure directories exist and write the TOML file
    try:
        with open(reinvent_config_path, "w") as f:
            f.write(toml_content)
        os.chmod(reinvent_config_path, 0o777)  # Set permissions for accessibility

        print(f"[DEBUG] TOML config created at {reinvent_config_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write TOML file: {e}")
        return {"task_id": task_id, "status": "error", "error": str(e)}

    # 🔍 Find running REINVENT container dynamically
    reinvent_container = "6d70f1227f4b"

    if not reinvent_container:
        print("[ERROR] REINVENT container is not running.")
        return {"task_id": task_id, "status": "error", "error": "REINVENT container not running"}

    # Run REINVENT inside the running container
    try:
        print("[DEBUG] Running REINVENT inside a new Docker container...")
        result = subprocess.run(
            [
                "docker", "exec", reinvent_container,
                "reinvent", "-l", log_path, reinvent_config_path
            ],
            capture_output=True,
            text=True
        )

        print("[DEBUG] REINVENT Execution Completed.")

        # Check if REINVENT ran successfully
        if result.returncode == 0:
            print(f"[DEBUG] Results file created at: {result_path}")
            return {
                "task_id": task_id,
                "status": "completed",
                "output_file": result_path,
                "json_output": json_out_path,  # ✅ Returning JSON output path
            }
        else:
            print(f"[ERROR] REINVENT Failed: {result.stderr}")
            return {"task_id": task_id, "status": "failed", "error": result.stderr}

    except Exception as e:
        print(f"[ERROR] Exception during execution: {e}")
        return {"task_id": task_id, "status": "error", "error": str(e)}
