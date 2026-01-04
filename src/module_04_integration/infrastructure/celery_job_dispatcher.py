import logging
from dataclasses import dataclass, field

from celery import Celery

from src.module_04_integration.domain.job_dispatcher import (
    Job,
    JobDispatcher,
    Payload,
)
from src.module_04_integration.infrastructure.celery_app import app

logger = logging.getLogger(__name__)


@dataclass
class CeleryJobDispatcher(JobDispatcher):
    """Celery job dispatcher."""

    _celery_app: Celery = field(default=app)
    _task_names: dict[str, str] = field(default_factory=dict, repr=False)

    def register(self, job_name: str, handler_name: str) -> None:
        """Register a job name to the given handler name."""
        self._task_names[job_name] = handler_name

    def dispatch(self, name: str, payload: Payload) -> Job:
        """Dispatch a task with the given payload."""
        task_name = self._task_names.get(name, name)
        data = payload.to_dict()
        task = self._celery_app.send_task(task_name, args=[data])

        return Job(
            name=name,
            id=task.id,
            payload=data,
        )
