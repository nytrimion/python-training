"""
Tests for UserService.

This file demonstrates:
- Using fixtures for dependency injection
- Mocking external services
- Testing exceptions with pytest.raises
"""

from unittest.mock import Mock

import pytest

from src.module_03_ecosysteme.exercice_01_pytest.notifications import NotificationResult
from src.module_03_ecosysteme.exercice_01_pytest.user_service import (
    UserService,
    UserValidationError,
)


class TestCreateUser:
    """Tests for user creation."""

    def test_create_user_success(self, user_service: UserService) -> None:
        """Test successful user creation."""
        user = user_service.create_user("alice@example.com", "Alice")

        assert user.id == 1
        assert user.email == "alice@example.com"
        assert user.name == "Alice"

    def test_create_user_invalid_email(self, user_service: UserService) -> None:
        """Test that invalid email raises UserValidationError."""
        with pytest.raises(UserValidationError, match="Invalid email"):
            user_service.create_user("invalid-email", "Alice")

    def test_create_user_duplicate_email(self, user_service: UserService) -> None:
        """Test that duplicate email raises UserValidationError."""
        user_service.create_user("alice@example.com", "Foo")

        with pytest.raises(
            UserValidationError, match="Email already registered: alice@example.com"
        ):
            user_service.create_user("alice@example.com", "Bar")


class TestCreateUserWithNotification:
    """Tests for user creation with notification."""

    def test_sends_welcome_email(
        self,
        user_service: UserService,
        mock_notification_service: Mock,
    ) -> None:
        """Test that welcome email is sent after user creation."""
        user, result = user_service.create_user_with_notification(
            "bob@example.com", "Bob"
        )

        # Verify user was created
        assert user.id is not None
        assert user.email == "bob@example.com"

        # Verify notification was sent
        assert result.success is True
        mock_notification_service.send_welcome_email.assert_called_once_with(
            email="bob@example.com",
            name="Bob",
        )

    def test_notification_failure_still_creates_user(
        self,
        user_service: UserService,
        mock_notification_service: Mock,
    ) -> None:
        """Test that user is created even if notification fails."""
        mock_notification_service.send_welcome_email.return_value = NotificationResult(
            success=False,
            error="SMTP connection failed",
        )
        user, result = user_service.create_user_with_notification(
            "bob@example.com",
            "Bob",
        )
        assert user.id is not None
        assert result.success is False
        assert "SMTP" in result.error


class TestGetUser:
    """Tests for user retrieval."""

    def test_get_user_by_id(self, user_service: UserService) -> None:
        """Test retrieving user by ID."""
        created = user_service.create_user("alice@example.com", "Alice")

        found = user_service.get_user(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.email == created.email

    def test_get_user_not_found(self, user_service: UserService) -> None:
        """Test that non-existent user returns None."""
        result = user_service.get_user(999)
        assert result is None

    def test_get_user_by_email(self, user_service: UserService) -> None:
        """Test retrieving user by email."""
        user_service.create_user("alice@example.com", "Alice")

        found = user_service.get_user_by_email("alice@example.com")

        assert found is not None
        assert found.name == "Alice"
