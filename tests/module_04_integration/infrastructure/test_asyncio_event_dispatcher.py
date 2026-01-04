import asyncio
from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from src.module_04_integration.domain.events import DomainEvent
from src.module_04_integration.infrastructure.asyncio_event_dispatcher import (
    AsyncioEventDispatcher,
)


@dataclass(kw_only=True)
class DummyEvent(DomainEvent):
    """Dummy event for testing."""

    @property
    def event_type(self) -> str:
        return "dummy.event"


@dataclass(kw_only=True)
class OtherDummyEvent(DomainEvent):
    """Other dummy event for testing."""

    @property
    def event_type(self) -> str:
        return "other.dummy.event"


class TestAsyncioEventDispatcher:
    """Test Asynchronous event dispatcher."""

    def setup_method(self):
        self.dispatcher = AsyncioEventDispatcher()

    def test_register_should_store_handler_for_event_type(self):
        """Test registering a single handler for an event type."""
        handler = AsyncMock()

        self.dispatcher.register(DummyEvent, handler)

        assert handler in self.dispatcher._handlers[DummyEvent]

    def test_register_should_allow_multiple_handlers_for_same_event_type(self):
        """Test registering multiple handlers for the same event type."""
        handler1 = AsyncMock()
        handler2 = AsyncMock()

        self.dispatcher.register(DummyEvent, handler1)
        self.dispatcher.register(DummyEvent, handler2)

        assert handler1 == self.dispatcher._handlers[DummyEvent][0]
        assert handler2 == self.dispatcher._handlers[DummyEvent][1]

    def test_register_should_allow_handlers_for_multiple_event_types(self):
        """Test registering handlers for multiple event types."""
        handler1 = AsyncMock()
        handler2 = AsyncMock()

        self.dispatcher.register(DummyEvent, handler1)
        self.dispatcher.register(OtherDummyEvent, handler2)

        assert handler1 == self.dispatcher._handlers[DummyEvent][0]
        assert handler2 == self.dispatcher._handlers[OtherDummyEvent][0]

    @pytest.mark.asyncio
    async def test_dispatch_should_call_all_handlers_for_event_type(self):
        """Test that dispatch calls all registered handlers for an event type."""
        handler1 = AsyncMock()
        handler2 = AsyncMock()
        event = DummyEvent()

        self.dispatcher.register(DummyEvent, handler1)
        self.dispatcher.register(DummyEvent, handler2)
        self.dispatcher.dispatch(event)

        await asyncio.sleep(0)
        handler1.assert_awaited_once_with(event)
        handler2.assert_awaited_once_with(event)

    def test_dispatch_without_handler_should_log_warning(self, mocker):
        """Test that dispatch logs warning when no handler is registered."""
        logger = mocker.patch(
            "src.module_04_integration.infrastructure.asyncio_event_dispatcher.logger",
        )
        event = DummyEvent()

        self.dispatcher.dispatch(event)

        logger.warning.assert_called_once_with(
            "No handler registered for event DummyEvent"
        )

    @pytest.mark.asyncio
    async def test_dispatch_should_continue_when_handler_raises_exception(self):
        """Test that dispatch continues to next handler when one fails."""
        handler1 = AsyncMock()
        handler1.side_effect = Exception("Handler error")
        handler2 = AsyncMock()
        event = DummyEvent()

        self.dispatcher.register(DummyEvent, handler1)
        self.dispatcher.register(DummyEvent, handler2)
        self.dispatcher.dispatch(event)

        await asyncio.sleep(0)
        handler1.assert_awaited_once_with(event)
        handler2.assert_awaited_once_with(event)
