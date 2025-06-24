from celery import Celery

celery_app = Celery(
    "reinvent_backend",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.autodiscover_tasks([
    "src.tasks.molecule_task",
    "src.tasks.transfer_learning"
])

# 🔥 Force import to trigger registration
# import src.tasks.transfer_learning