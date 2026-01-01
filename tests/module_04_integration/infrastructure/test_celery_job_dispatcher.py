from dataclasses import dataclass, field
from typing import Self
from unittest.mock import Mock, ANY

import pytest

from src.module_04_integration.domain.types import JsonDict
from src.module_04_integration.infrastructure.celery_job_dispatcher import CeleryJobDispatcher


@dataclass(kw_only=True)
class DummyPayload:
    """Dummy payload for testing."""
    data: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return self.data


class TestCeleryJobDispatcher:
    """Test Celery job dispatcher."""

    def setup_method(self):
        self.dispatcher = CeleryJobDispatcher()

    @pytest.fixture
    def mock_send_task(self, mocker):
        mock_task = Mock()
        mock_task.id = "task-id"
        return mocker.patch.object(
            self.dispatcher._celery_app,
            "send_task",
            return_value=mock_task,
        )

    def test_register_maps_job_name_to_task_name(self):
        """Test registering task name for job name."""
        self.dispatcher.register("job", "task")

        assert "job" in self.dispatcher._task_names
        assert self.dispatcher._task_names["job"] == "task"

    def test_dispatch_sends_task_with_payload(self, mock_send_task):
        """Test dispatching task with payload."""
        self.dispatcher.dispatch("job", DummyPayload(data={"foo": "bar"}))

        mock_send_task.assert_called_once_with("job", args=[{"foo": "bar"}])

    def test_dispatch_returns_job_with_expected_properties(self, mock_send_task):
        """Test dispatching job with expected properties."""
        job = self.dispatcher.dispatch("job", DummyPayload(data={"foo": "bar"}))

        assert job.name == "job"
        assert job.id == "task-id"
        assert job.payload == {"foo": "bar"}

    def test_dispatch_uses_registered_task_name(self, mock_send_task):
        """Test dispatch uses registered task name."""
        self.dispatcher.register("job", "task")
        self.dispatcher.dispatch("job", DummyPayload())

        mock_send_task.assert_called_once_with("task", args=ANY)

    def test_dispatch_uses_job_name_as_default_task_name(self, mock_send_task):
        """Test dispatch uses job name as default task name."""
        self.dispatcher.dispatch("job", DummyPayload())

        mock_send_task.assert_called_once_with("job", args=ANY)
