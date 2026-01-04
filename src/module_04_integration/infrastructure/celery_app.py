from celery import Celery

# Create Celery app with Redis
app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

# Configuration
app.conf.update(
    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    # Timezone
    timezone="Europe/Paris",
    enable_utc=True,
    # Reliability
    task_acks_late=True,  # ACK after execution (not before)
    task_reject_on_worker_lost=True,  # Requeue if worker crashes
    # Result expiration (1 hour)
    result_expires=3600,
)
