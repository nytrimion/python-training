import asyncio

from src.module_04_integration.application import event_handlers
from src.module_04_integration.domain import events
from src.module_04_integration.domain.types import JsonDict
from src.module_04_integration.infrastructure.celery_app import app


@app.task(max_retries=3, default_retry_delay=10)
def verify_account_email(payload: JsonDict) -> None:
    """Verify account email task."""
    event = events.AccountCreatedEvent.from_dict(payload)
    handler = event_handlers.VerifyAccountEmailHandler()
    asyncio.run(handler(event))
