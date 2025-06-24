import os
from pathlib import Path

BASE_PATH = Path("/app/projects")

def create_project_dir(project_id: str):
    project_path = BASE_PATH / project_id
    (project_path / "input").mkdir(parents=True, exist_ok=True)
    (project_path / "models").mkdir(parents=True, exist_ok=True)
    (project_path / "runs").mkdir(parents=True, exist_ok=True)

def save_smiles_file(project_id: str, file):
    input_dir = BASE_PATH / project_id / "input"
    file_path = input_dir / "train.csv"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
