"""
Tests for Celery tasks demonstrating 4 testing strategies.

This demonstrates:
- Eager mode for integration tests
- Direct function calls for unit tests
- Mocking for testing calling code
- Retry behavior testing
"""
import pytest
from celery.exceptions import Retry
from unittest.mock import MagicMock, ANY

from src.module_03_ecosysteme.exercice_03_celery.tasks import (
    send_confirmation_email,
    EmailError,
    PermanentEmailError,
)


class TestEagerMode:
    """
    Test tasks using Celery's eager mode.

    Eager mode executes tasks synchronously in the same process,
    allowing full integration tests without a worker.
    """

    def test_send_email_success_eager_mode(self, celery_eager_mode, mocker) -> None:
        """Test task execution through .delay() with eager mode."""
        mocker.patch(
            "src.module_03_ecosysteme.exercice_03_celery.tasks._simulate_email_send",
            return_value="test-message-id",
        )
        result = send_confirmation_email.delay("test@example.com", "order-id").get()

        assert result["status"] == "sent"
        assert result["message_id"] == "test-message-id"
        assert result["to"] == "test@example.com"


class TestDirectCall:
    """
    Test task logic by calling the function directly.

    This bypasses Celery entirely and tests pure business logic.
    """

    def test_send_email_success_direct(self, mocker) -> None:
        """Test task logic with successful email sending."""
        mocker.patch(
            "src.module_03_ecosysteme.exercice_03_celery.tasks._simulate_email_send",
            return_value="test-message-id",
        )
        result = send_confirmation_email("test@example.com", "order-id")

        assert result["status"] == "sent"
        assert result["message_id"] == "test-message-id"
        assert result["to"] == "test@example.com"

    def test_send_email_permanent_failure_direct(self, mocker) -> None:
        """Test task logic with permanent email failure."""
        mocker.patch(
            "src.module_03_ecosysteme.exercice_03_celery.tasks._simulate_email_send",
            side_effect=PermanentEmailError("error-message"),
        )
        result = send_confirmation_email("test@example.com", "order-id")

        assert result["status"] == "failed"
        assert result["error"] == "error-message"
        assert result["to"] == "test@example.com"


class TestMocking:
    """
    Test code that triggers Celery tasks by mocking the task.

    This isolates the calling code from Celery entirely.
    """

    def test_create_order_triggers_email_task(self, client, mocker) -> None:
        """Test that POST /orders triggers the email task."""
        mock_task = MagicMock()
        mock_task.id = "mock-task-id"

        mock_delay = mocker.patch(
            "src.module_03_ecosysteme.exercice_03_celery.app.send_confirmation_email.delay",
            return_value=mock_task,
        )

        response = client.post("/orders", json={
            "product": "",
            "quantity": 3,
            "customer_email": "test@example.com",
        })

        assert response.json()["email_task_id"] == "mock-task-id"
        assert mock_delay.called
        assert mock_delay.call_args.args[0] == "test@example.com"
        mock_delay.assert_called_once_with("test@example.com", ANY)


class TestRetryBehavior:
    """
    Test retry behavior when tasks fail with temporary errors.

    This requires eager mode with task_eager_propagates=True to catch Retry exceptions.
    """

    def test_send_email_retries_on_transient_error(
            self,
            celery_eager_mode,
            mocker,
    ) -> None:
        """Test that EmailError triggers a retry."""
        mocker.patch(
            "src.module_03_ecosysteme.exercice_03_celery.tasks._simulate_email_send",
            side_effect=EmailError("Connection timeout"),
        )
        with pytest.raises(Retry) as exc:
            send_confirmation_email.delay("test@example.com", "order-id").get()

        assert isinstance(exc.value.exc, EmailError)
        assert str(exc.value.exc) == "Connection timeout"
        assert exc.value.when == 10
