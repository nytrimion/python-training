"""
Shared fixtures for Celery tests.

This demonstrates:
- Eager mode configuration for synchronous testing
- FastAPI TestClient setup
- Mocking utilities for Celery tasks
"""

import pytest
from fastapi.testclient import TestClient

from src.module_03_ecosysteme.exercice_03_celery.app import app as fastapi_app
from src.module_03_ecosysteme.exercice_03_celery.celery_app import app as celery_app


@pytest.fixture
def _celery_eager_mode():
    """
    Configure Celery to run tasks synchronously.

    This is useful for integration tests where you want tasks
    to execute immediately without a worker.
    """
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
def client() -> TestClient:
    """FastAPI test client for endpoint testing."""
    return TestClient(fastapi_app)
