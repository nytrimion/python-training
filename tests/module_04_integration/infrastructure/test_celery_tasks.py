from unittest.mock import AsyncMock

from src.module_04_integration.infrastructure.celery_tasks import verify_account_email


class TestVerifyAccountEmail:
    """Test verify account email task logic"""

    def test_verify_account_email_calls_event_handler_in_eager_mode(
            self,
            account_created_event,
            _celery_eager_mode,
            mocker,
    ):
        """Test verify_account_email task calls event handler in eager mode."""
        mock_handler = AsyncMock()
        mocker.patch(
            "src.module_04_integration.infrastructure.celery_tasks.event_handlers.VerifyAccountEmailHandler",
            return_value=mock_handler,
        )
        verify_account_email.delay(account_created_event.to_dict())

        mock_handler.assert_called_once_with(account_created_event)

    def test_verify_account_email_calls_event_handler_from_direct_call(
            self,
            account_created_event,
            mocker,
    ):
        """Test verify_account_email task calls event handler from direct call."""
        mock_handler = AsyncMock()
        mocker.patch(
            "src.module_04_integration.infrastructure.celery_tasks.event_handlers.VerifyAccountEmailHandler",
            return_value=mock_handler,
        )
        verify_account_email(account_created_event.to_dict())

        mock_handler.assert_called_once_with(account_created_event)
