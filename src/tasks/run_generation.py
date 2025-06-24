#  tasks/run_generation.py
import subprocess
import os
from pathlib import Path
import uuid
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, QED

PROJECT_ROOT = Path(os.environ.get("PROJECT_DIR", "/app/projects"))

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


def run_sampling_from_agent(project_id: str):
    run_id = f"run_{uuid.uuid4().hex}"
    run_path = PROJECT_ROOT / project_id / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)

    model_file = PROJECT_ROOT / project_id / "models/agent.pt"
    raw_output = run_path / "raw_results.csv"
    json_output = run_path / "sampling.json"
    config_path = run_path / "config.toml"
    log_path = run_path / "sample.log"

    toml_content = f"""
run_type = \"sampling\"
device = \"cpu\"
json_out_config = \"{json_output}\"

[parameters]
model_file = \"{model_file}\"
output_file = \"{raw_output}\"
num_smiles = 128
unique_molecules = true
randomize_smiles = true
"""

    with open(config_path, "w") as f:
        f.write(toml_content)

    subprocess.run([
        "docker", "exec", "centella-reinvent-backend-reinvent",
        "reinvent", "-l", str(log_path), str(config_path)
    ])

    try:
        df = pd.read_csv(raw_output)
        df = compute_descriptors(df["SMILES"].tolist())
        scored_output = run_path / "results.csv"
        df.to_csv(scored_output, index=False)
    except Exception as e:
        with open(run_path / "error.log", "w") as err:
            err.write(str(e))
