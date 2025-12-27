from abc import ABC
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any
import uuid


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

    def to_dict(self) -> dict[str, Any]:
        """Serialize event for queue transport."""
        return {k: self._serialize(v) for k, v in asdict(self).items()}


@dataclass(kw_only=True)
class AccountCreatedEvent(DomainEvent):
    """Domain Event for account creation."""
    account_id: str
    email: str
