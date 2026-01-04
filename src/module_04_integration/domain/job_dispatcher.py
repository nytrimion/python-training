from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from src.module_04_integration.domain.types import JsonDict


class Payload(Protocol):
    """Something that can be serialized to JSON-compatible dict."""

    def to_dict(self) -> JsonDict: ...


@dataclass(kw_only=True, frozen=True)
class Job:
    """Job."""

    name: str
    id: str
    payload: JsonDict = field(default_factory=dict)


class JobDispatcher(ABC):
    """Abstract interface for distributed job dispatching."""

    @abstractmethod
    def register(self, job_name: str, handler_name: str) -> None:
        """Register a job name to the given handler name."""
        pass

    @abstractmethod
    def dispatch(self, name: str, payload: Payload) -> Job:
        """Dispatch a task with the given payload."""
        pass
