from src.module_04_integration.domain.event_dispatcher import EventDispatcher
from src.module_04_integration.domain.job_dispatcher import JobDispatcher
from src.module_04_integration.infrastructure.dependencies import (
    get_event_dispatcher,
    get_job_dispatcher,
)


class TestGetEventDispatcher:
    """Test event dispatcher factory."""

    def test_it_returns_event_dispatcher(self):
        """Test the factory returns an event dispatcher."""
        assert isinstance(get_event_dispatcher(), EventDispatcher)

    def test_it_returns_singleton(self):
        """Test the factory returns a singleton."""
        dispatcher1 = get_event_dispatcher()
        dispatcher2 = get_event_dispatcher()

        assert dispatcher1 is dispatcher2


class TestGetJobDispatcher:
    """Test job dispatcher factory."""

    def test_it_returns_job_dispatcher(self):
        """Test the factory returns a job dispatcher."""
        assert isinstance(get_job_dispatcher(), JobDispatcher)

    def test_it_returns_singleton(self):
        """Test the factory returns a singleton."""
        dispatcher1 = get_job_dispatcher()
        dispatcher2 = get_job_dispatcher()

        assert dispatcher1 is dispatcher2
