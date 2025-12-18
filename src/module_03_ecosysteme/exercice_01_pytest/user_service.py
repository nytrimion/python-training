"""
User service demonstrating typical business logic patterns.
"""

from .models import User
from .notifications import NotificationResult, NotificationService
from .validators import validate_email, validate_name


class UserValidationError(Exception):
    """Raised when user validation fails."""

    pass


class UserService:
    """
    Service for user-related operations.

    This service demonstrates dependency injection pattern:
    - Repository for persistence (simulated with in-memory dict)
    - NotificationService for sending emails
    """

    def __init__(self, notification_service: NotificationService) -> None:
        self.notification_service = notification_service
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, email: str, name: str) -> User:
        """
        Create a new user with validation.

        Args:
            email: User's email address
            name: User's display name

        Returns:
            The created User with assigned ID

        Raises:
            UserValidationError: If email or name is invalid
        """
        if not validate_email(email):
            raise UserValidationError(f"Invalid email format: {email}")

        if not validate_name(name):
            raise UserValidationError(f"Invalid name: {name}")

        if self._email_exists(email):
            raise UserValidationError(f"Email already registered: {email}")

        user = User(email=email, name=name).with_id(self._next_id)
        self._users[user.id] = user
        self._next_id += 1

        return user

    def create_user_with_notification(
            self, email: str, name: str
    ) -> tuple[User, NotificationResult]:
        """
        Create a user and send welcome email.

        Args:
            email: User's email address
            name: User's display name

        Returns:
            Tuple of (created User, NotificationResult)
        """
        user = self.create_user(email, name)
        notification_result = self.notification_service.send_welcome_email(
            email=user.email,
            name=user.name,
        )
        return user, notification_result

    def get_user(self, user_id: int) -> User | None:
        """Get user by ID."""
        return self._users.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def _email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        return any(u.email == email for u in self._users.values())
