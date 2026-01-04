import asyncio
import logging
from dataclasses import dataclass, field

from src.module_04_integration.domain.event_dispatcher import (
    EventDispatcher,
    EventHandler,
)
from src.module_04_integration.domain.events import DomainEvent

logger = logging.getLogger(__name__)


@dataclass
class SyncEventDispatcher(EventDispatcher):
    """Synchronous event dispatcher."""

    _handlers: dict[type[DomainEvent], list[EventHandler[DomainEvent]]] = field(
        default_factory=dict,
        repr=False,
    )

    def register(
            self,
            event_type: type[DomainEvent],
            handler: EventHandler[DomainEvent],
    ) -> None:
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
            try:
                asyncio.run(handler(event))
            except Exception as e:
                logger.error(f"Event handler {type(handler).__name__} failed: {e}")
