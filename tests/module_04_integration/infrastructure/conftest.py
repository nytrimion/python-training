import pytest

from src.module_04_integration.domain.events import AccountCreatedEvent
from src.module_04_integration.infrastructure.celery_app import app as celery_app


@pytest.fixture
def _celery_eager_mode():
    """Configure Celery to run tasks synchronously."""
    # Store original settings
    original_eager = celery_app.conf.task_always_eager
    original_propagates = celery_app.conf.task_eager_propagates

    # Enable eager mode
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True

    yield celery_app

    # Restore original settings
    celery_app.conf.task_always_eager = original_eager
    celery_app.conf.task_eager_propagates = original_propagates


@pytest.fixture
def account_created_event():
    """Configure an account created event."""
    yield AccountCreatedEvent(
        account_id="account_id",
        email="test@example.com",
    )
