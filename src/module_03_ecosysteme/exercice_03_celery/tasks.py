"""
Celery tasks for email notifications.

This module demonstrates:
- Basic task definition
- Task with retry and exponential backoff
- Simulated email sending (would be real SMTP in production)
"""

from __future__ import annotations
import logging
import random
from datetime import datetime
from typing import Any

from celery import Task

from .celery_app import app

logger = logging.getLogger(__name__)


class EmailError(Exception):
    """Raised when email sending fails (temporary error, can retry)."""

    pass


class PermanentEmailError(Exception):
    """Raised when email sending fails permanently (don't retry)."""

    pass


def _simulate_email_send(to: str, _subject: str, _body: str) -> str:
    """
    Simulate email sending with random failures for testing.

    In production, this would call a real SMTP server or email API.

    Returns:
        Message ID on success

    Raises:
        EmailError: Temporary failure (should retry)
        PermanentEmailError: Permanent failure (don't retry)
    """
    # Simulate random failures for testing retry logic
    failure_chance = random.random()

    if failure_chance < 0.3:  # 30% temporary failure
        logger.warning(f"Temporary email failure to {to}")
        raise EmailError("SMTP server temporarily unavailable")

    if failure_chance < 0.35:  # 5% permanent failure
        logger.error(f"Permanent email failure to {to}")
        raise PermanentEmailError("Invalid email address format")

    # Success
    message_id = (
        f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
    )
    logger.info(f"Email sent to {to}, message_id={message_id}")
    return message_id


@app.task(bind=True, max_retries=3, default_retry_delay=10)
def send_confirmation_email(
        self: Task[Any],  # type: ignore[type-arg]
        email: str,
        order_id: str,
) -> dict[str, Any]:
    """
    Send order confirmation email with retry on temporary failures.

    Args:
        self: Celery task
        email: Recipient email address
        order_id: Order ID for the confirmation

    Returns:
        Dict with status, message_id (on success), or error (on failure)
    """
    retries = self.request.retries
    logger.info(f"Sending confirmation email to {email}, attempt {retries + 1}")

    subject = f"Order Confirmation - {order_id}"
    body = f"Thank you for your order {order_id}!"

    try:
        message_id = _simulate_email_send(email, subject, body)
        return {
            "status": "sent",
            "message_id": message_id,
            "to": email,
        }
    except EmailError as exc:
        raise self.retry(exc=exc, countdown=10 * (2 ** retries)) from exc
    except PermanentEmailError as exc:
        return {
            "status": "failed",
            "error": str(exc),
            "to": email,
        }
