from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from src.module_04_integration.domain.events import DomainEvent

E = TypeVar("E", bound=DomainEvent, contravariant=True)


class EventHandler(Protocol[E]):
    """Event handler type."""

    async def __call__(self, event: E) -> None: ...


class EventDispatcher(ABC):
    """Abstract interface for event dispatching."""

    @abstractmethod
    def register(
            self,
            event_type: type[DomainEvent],
            handler: EventHandler[DomainEvent],
    ) -> None:
        """Register an event type to the given handler."""
        pass

    @abstractmethod
    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event to its handlers."""
        pass
