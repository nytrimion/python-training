import logging

from src.module_04_integration.domain.events import AccountCreatedEvent

logger = logging.getLogger(__name__)


class VerifyAccountEmailHandler:
    async def __call__(self, event: AccountCreatedEvent) -> None:
        """Verify account email on account created event."""
        logger.info(f"Account verification email sent to {event.email}")
