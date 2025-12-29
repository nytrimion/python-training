import asyncio
from dataclasses import dataclass, field
import logging

from src.module_04_integration.domain.events import DomainEvent
from src.module_04_integration.domain.event_dispatcher import (
    EventDispatcher,
    EventHandler,
)

logger = logging.getLogger(__name__)


@dataclass
class AsyncioEventDispatcher(EventDispatcher):
    """Asynchronous event dispatcher."""
    _handlers: dict[type[DomainEvent], list[EventHandler]] = field(
        default_factory=dict,
        repr=False,
    )

    async def _safe_call_handler(self, handler: EventHandler, event: DomainEvent) -> None:
        """Execute handler with error handling."""
        try:
            await handler(event)
        except Exception as e:
            logger.error(f"Event handler {type(handler).__name__} failed: {e}")

    def register(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        """Register an event type to the given handler."""
        self._handlers.setdefault(event_type, []).append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch event to handlers."""
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        if not handlers:
            logger.warning(f"No handler registered for event {event_type.__name__}")
            return

        for handler in handlers:
            asyncio.create_task(self._safe_call_handler(handler, event))
