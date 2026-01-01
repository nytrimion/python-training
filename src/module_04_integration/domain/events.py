from abc import ABC
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Self
import uuid

from src.module_04_integration.domain.types import JsonDict


@dataclass(kw_only=True)
class DomainEvent(ABC):
    """Abstract Domain Event."""
    event_id: uuid.UUID = field(default_factory=lambda: uuid.uuid7())
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def _serialize(self, value: Any) -> Any:
        """Convert non-JSON-serializable types."""
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def to_dict(self) -> JsonDict:
        """Serialize event for queue transport."""
        return {k: self._serialize(v) for k, v in asdict(self).items()}

    @classmethod
    def from_dict(cls, data: JsonDict) -> Self:
        """Reconstruct event from serialized dict."""
        transformed = {
            **data,
            "event_id": uuid.UUID(data["event_id"]),
            "occurred_at": datetime.fromisoformat(data["occurred_at"]),
        }
        return cls(**transformed)


@dataclass(kw_only=True)
class AccountCreatedEvent(DomainEvent):
    """Domain Event for account creation."""
    account_id: str
    email: str
