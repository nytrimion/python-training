"""
Notification service (to be mocked in tests).
"""

from dataclasses import dataclass


@dataclass
class NotificationResult:
    """Result of a notification attempt."""

    success: bool
    message_id: str | None = None
    error: str | None = None


class NotificationService:
    """
    Service for sending notifications.

    In production, this would connect to an email provider, SMS gateway, etc.
    For testing, we'll mock this entirely.
    """

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def send_welcome_email(self, email: str, name: str) -> NotificationResult:
        """
        Send a welcome email to a new user.

        In production, this would actually send an email.
        """
        # Simulate API call - in real code, this would be an HTTP request
        raise NotImplementedError(
            "This should be mocked in tests! "
            "In production, implement actual email sending."
        )

    def send_password_reset(self, email: str, reset_token: str) -> NotificationResult:
        """Send a password reset email."""
        raise NotImplementedError("This should be mocked in tests!")
