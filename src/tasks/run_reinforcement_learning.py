import subprocess
import os
from pathlib import Path
import uuid

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))


def run_reinforcement_learning_task(project_id: str):
    run_id = f"run_{uuid.uuid4().hex}"
    run_path = PROJECT_ROOT / project_id / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)

    agent_model = PROJECT_ROOT / project_id / "models/agent.pt"
    prior_model = "priors/reinvent.prior"
    output_csv = run_path / "results.csv"
    json_output = run_path / "sampling.json"
    config_path = run_path / "config.toml"
    log_path = run_path / "reinforce.log"

    toml_content = f"""
run_type = \"reinforcement_learning\"
device = \"cpu\"
json_out_config = \"{json_output}\"

[parameters]
prior = \"{prior_model}\"
agent = \"{agent_model}\"
output_file = \"{output_csv}\"
num_smiles = 256
batch_size = 64
sigma = 128.0
"""

    with open(config_path, "w") as f:
        f.write(toml_content)

    subprocess.run([
        "docker", "exec", "centella-reinvent-backend-reinvent",
        "reinvent", "-l", str(log_path), str(config_path)
    ])