"""
Simple domain models for testing exercise.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Self


@dataclass
class User:
    """User entity."""

    email: str
    name: str
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def with_id(self, id: int) -> Self:
        """Return a copy with the given ID."""
        return type(self)(
            id=id,
            email=self.email,
            name=self.name,
            created_at=self.created_at,
        )
