from celery import Celery
import subprocess
import os
from pathlib import Path
import uuid

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

@celery_app.task(name="src.tasks.reinforcement_learning.run_reinforcement_learning_task")
def run_reinforcement_learning_task(project_id: str):
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
    tb_logdir = run_path / "tb"
    stage1_checkpoint = run_path / "stage1.chkpt"

    toml_content = f"""
run_type = "staged_learning"
device = "cpu"
tb_logdir = "{tb_logdir}"
json_out_config = "{json_output}"

[parameters]
prior_file = "{prior_model}"
agent_file = "{agent_model}"
summary_csv_prefix = "stage1"
batch_size = 64
use_checkpoint = true

[learning_strategy]
type = "dap"
sigma = 128.0
rate = 0.0001

[[stage]]
max_score = 1.0
max_steps = 300
chkpt_file = "{stage1_checkpoint}"
scoring_function.type = "custom_product"

[stage.scoring]
type = "geometric_mean"

[[stage.scoring.component]]
[stage.scoring.component.custom_alerts]

[[stage.scoring.component.custom_alerts.endpoint]]
name = "Alerts"
params.smarts = [
    "[*;r8]", "[*;r9]", "[*;r10]", "[*;r11]", "[*;r12]", "[*;r13]",
    "[*;r14]", "[*;r15]", "[*;r16]", "[*;r17]", "[#8][#8]", "[#6;+]",
    "[#16][#16]", "[#7;!n][S;!$(S(=O)=O)]", "[#7;!n][#7;!n]", "C#C",
    "C(=[O,S])[O,S]", "[#7;!n][C;!$(C(=[O,N])[N,O])][#16;!s]",
    "[#7;!n][C;!$(C(=[O,N])[N,O])][#7;!n]",
    "[#7;!n][C;!$(C(=[O,N])[N,O])][#8;!o]",
    "[#8;!o][C;!$(C(=[O,N])[N,O])][#16;!s]",
    "[#8;!o][C;!$(C(=[O,N])[N,O])][#8;!o]",
    "[#16;!s][C;!$(C(=[O,N])[N,O])][#16;!s]"
]

[[stage.scoring.component]]
[stage.scoring.component.QED]
[[stage.scoring.component.QED.endpoint]]
name = "QED"
weight = 0.6

[[stage.scoring.component]]
[stage.scoring.component.NumAtomStereoCenters]
[[stage.scoring.component.NumAtomStereoCenters.endpoint]]
name = "Stereo"
weight = 0.4

transform.type = "left_step"
transform.low = 0
"""

    try:
        with open(config_path, "w") as f:
            f.write(toml_content)
        print(f"[INFO] TOML config written at: {config_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write TOML: {e}")
        return

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
