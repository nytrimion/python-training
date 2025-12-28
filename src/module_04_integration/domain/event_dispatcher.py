from abc import ABC, abstractmethod
from typing import Protocol

from src.module_04_integration.domain.events import DomainEvent


class EventHandler(Protocol):
    """Event handler type."""

    def __call__(self, event: DomainEvent) -> None: ...


class EventDispatcher(ABC):
    """Abstract interface for event dispatching."""

    @abstractmethod
    def register(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        """Register an event type to the given handler."""
        pass

    @abstractmethod
    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event to its handlers."""
        pass
