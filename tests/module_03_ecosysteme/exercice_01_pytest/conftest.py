"""
Shared fixtures for exercise 01 tests.

This file is automatically discovered by pytest.
Fixtures defined here are available to all tests in this directory.
"""

import pytest
from unittest.mock import Mock

from src.module_03_ecosysteme.exercice_01_pytest.notifications import (
    NotificationService,
    NotificationResult,
)
from src.module_03_ecosysteme.exercice_01_pytest.user_service import UserService


@pytest.fixture
def mock_notification_service() -> Mock:
    """
    Create a mock NotificationService.

    The mock is pre-configured with a successful send_welcome_email response.
    Tests can override this behavior as needed.
    """
    mock = Mock(spec=NotificationService)
    mock.send_welcome_email.return_value = NotificationResult(
        success=True,
        message_id="msg_123",
    )
    mock.send_password_reset.return_value = NotificationResult(
        success=True,
        message_id="msg_456",
    )
    return mock


@pytest.fixture
def user_service(mock_notification_service: Mock) -> UserService:
    """Create a UserService with mocked dependencies."""
    return UserService(mock_notification_service)
