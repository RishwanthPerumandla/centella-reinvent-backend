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
    """Runs the molecule design pipeline using REINVENT as a dynamically triggered container"""

    task_id = task_data.get("task_id", f"task_{uuid.uuid4().hex}")
    device = task_data.get("device", "cpu")
    model_file = task_data.get("model_file", "priors/reinvent.prior")
    num_smiles = task_data.get("num_smiles", 157)
    unique_molecules = task_data.get("unique_molecules", True)
    randomize_smiles = task_data.get("randomize_smiles", True)

    print(f"[DEBUG] Task ID: {task_id}")

    # Define paths
    reinvent_config_path = f"reinvent/configs/{task_id}.toml"
    result_path = f"results/{task_id}.csv"

    print(f"[DEBUG] Writing config file to: {reinvent_config_path}")

    # Create a TOML config file dynamically
    toml_content = f"""
run_type = "sampling"
device = "{device}"
json_out_config = "_sampling.json"

[parameters]
model_file = "{model_file}"
output_file = "{result_path}"

num_smiles = {num_smiles}
unique_molecules = {str(unique_molecules).lower()}
randomize_smiles = {str(randomize_smiles).lower()}
"""

    # Ensure directories exist and write the TOML file
    try:
    # Ensure directories exist and write the TOML file
        os.makedirs(os.path.dirname(reinvent_config_path), exist_ok=True)
        with open(reinvent_config_path, "w") as f:
            f.write(toml_content)

        # Set permissions to allow all users to read/write
        os.chmod(reinvent_config_path, 0o777)  
        
        print(f"[DEBUG] TOML config created at {reinvent_config_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write TOML file: {e}")
        return {"task_id": task_id, "status": "error", "error": str(e)}


    # Run REINVENT dynamically as a new container
    try:
        print("[DEBUG] Running REINVENT inside a new Docker container...")
  

# Run REINVENT inside the running container
        result = subprocess.run(
            [
                "docker", "exec", "centella-reinvent-backend-reinvent-1",
                "reinvent", "-l", f"/app/reinvent/logs/{task_id}.log", f"/app/reinvent/configs/{task_id}.toml"
            ],
            capture_output=True,
            text=True
        )

        print("[DEBUG] REINVENT Execution Completed.")

        # Check if REINVENT ran successfully
        if result.returncode == 0:
            print(f"[DEBUG] Results file created at: {result_path}")
            return {"task_id": task_id, "status": "completed", "output_file": result_path}
        else:
            print(f"[ERROR] REINVENT Failed: {result.stderr}")
            return {"task_id": task_id, "status": "failed", "error": result.stderr}

    except Exception as e:
        print(f"[ERROR] Exception during execution: {e}")
        return {"task_id": task_id, "status": "error", "error": str(e)}
