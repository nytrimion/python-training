from ..application.event_handlers import TrackNewAccountHandler
from ..domain.event_dispatcher import EventDispatcher
from ..domain.events import AccountCreatedEvent
from ..domain.job_dispatcher import JobDispatcher
from .asyncio_event_dispatcher import AsyncioEventDispatcher
from .celery_job_dispatcher import CeleryJobDispatcher

_event_dispatcher = AsyncioEventDispatcher()
_event_dispatcher.register(AccountCreatedEvent, TrackNewAccountHandler())  # type: ignore[arg-type]


def get_event_dispatcher() -> EventDispatcher:
    return _event_dispatcher


_job_dispatcher = CeleryJobDispatcher()
_job_dispatcher.register("verify_account_email", "verify_account_email")


def get_job_dispatcher() -> JobDispatcher:
    return _job_dispatcher
