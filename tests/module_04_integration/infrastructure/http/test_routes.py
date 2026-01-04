import uuid
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from src.module_04_integration.domain.events import AccountCreatedEvent
from src.module_04_integration.infrastructure.dependencies import (
    get_event_dispatcher,
    get_job_dispatcher,
)
from src.module_04_integration.infrastructure.http.app import app


@pytest.fixture
def mock_event_dispatcher():
    return Mock()


@pytest.fixture
def mock_job_dispatcher():
    mock_job_dispatcher = Mock()
    mock_job_dispatcher.dispatch.return_value = Mock(id="job-id")
    return mock_job_dispatcher


@pytest.fixture
def client(mock_event_dispatcher, mock_job_dispatcher):
    app.dependency_overrides[get_event_dispatcher] = lambda: mock_event_dispatcher
    app.dependency_overrides[get_job_dispatcher] = lambda: mock_job_dispatcher
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_account(client, mock_event_dispatcher, mock_job_dispatcher):
    """Test the account creation endpoint."""
    response = client.post("/accounts", json={"email": "test@example.com"})

    mock_event_dispatcher.dispatch.assert_called_once()
    event = mock_event_dispatcher.dispatch.call_args[0][0]
    assert isinstance(event, AccountCreatedEvent)
    assert uuid.UUID(event.account_id).version == 7
    assert event.email == "test@example.com"

    mock_job_dispatcher.dispatch.assert_called_once_with("verify_account_email", event)

    assert response.status_code == 200
    assert response.json() == {
        "account_id": event.account_id,
        "status": "pending",
        "message": "Account verification pending",
        "verification_job_id": "job-id",
    }
