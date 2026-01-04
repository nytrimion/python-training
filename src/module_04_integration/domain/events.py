import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Self

from src.module_04_integration.domain.types import JsonDict


@dataclass(kw_only=True)
class DomainEvent(ABC):
    """Abstract Domain Event."""

    event_id: uuid.UUID = field(default_factory=lambda: uuid.uuid7())  # type: ignore[attr-defined]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def _serialize(self, value: Any) -> Any:
        """Convert non-JSON-serializable types."""
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Return the event type identifier."""
        pass

    def to_dict(self) -> JsonDict:
        """Serialize event for queue transport."""
        return {k: self._serialize(v) for k, v in asdict(self).items()}

    @classmethod
    def from_dict(cls, data: JsonDict) -> Self:
        """Reconstruct event from serialized dict."""
        transformed = {
            **data,
            "event_id": uuid.UUID(str(data["event_id"])),
            "occurred_at": datetime.fromisoformat(str(data["occurred_at"])),
        }
        return cls(**transformed)  # type: ignore[arg-type]


@dataclass(kw_only=True)
class AccountCreatedEvent(DomainEvent):
    """Domain Event for account creation."""

    account_id: str
    email: str

    @property
    def event_type(self) -> str:
        return "account.created"
