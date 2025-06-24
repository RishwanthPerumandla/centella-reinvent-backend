import subprocess
import os
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))

def run_transfer_learning_task(project_id: str):
    project_path = PROJECT_ROOT / project_id
    input_path = project_path / "input"
    model_path = project_path / "models"
    config_path = project_path / "config.toml"

    model_in = "priors/reinvent.prior"
    model_out = model_path / "agent.pt"
    train_file = input_path / "train.csv"

    # Ensure necessary directories exist
    input_path.mkdir(parents=True, exist_ok=True)
    model_path.mkdir(parents=True, exist_ok=True)

    # Build TOML content
    toml_content = f"""
run_type = "transfer_learning"
device = "cpu"

[parameters]
model_file = "{model_in}"
input_smiles_path = "{train_file}"
output_model_path = "{model_out}"
num_epochs = 10
batch_size = 128
max_steps = 1000
"""

    try:
        with open(config_path, "w") as f:
            f.write(toml_content)
        print(f"[INFO] TOML config written at: {config_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write TOML: {e}")
        return

    # Run REINVENT
    try:
        subprocess.run([
            "reinvent",
            "-l", str(project_path / "train.log"),
            str(config_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] REINVENT training failed: {e}")
