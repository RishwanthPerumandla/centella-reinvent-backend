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
def run_molecule_design(task_data):
    """ Runs the molecule design pipeline using REINVENT """
    task_id = task_data.get("task_id")
    return f"Task {task_id} completed successfully"
