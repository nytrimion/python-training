import uuid
from datetime import UTC, datetime

from src.module_04_integration.domain.events import AccountCreatedEvent


class TestAccountCreatedEvent:
    """Test the account creation event."""

    def setup_method(self):
        self.event = AccountCreatedEvent(
            account_id="account-id",
            email="test@example.com",
        )

    def test_event_type_property_has_expected_value(self):
        """Test the event type property has the expected value."""
        assert self.event.event_type == "account.created"

    def test_event_id_property_has_uuid_default_value(self):
        """Test the event id property has random UUID as default value."""
        assert isinstance(self.event.event_id, uuid.UUID)
        assert self.event.event_id.version == 7

    def test_occurred_at_property_has_datetime_default_value(self):
        """Test the occurred at property has UTC datetime as default value."""
        assert isinstance(self.event.occurred_at, datetime)
        assert self.event.occurred_at.tzname() == "UTC"

    def test_account_id_property_has_given_value(self):
        """Test the account id property has the given value."""
        assert self.event.account_id == "account-id"

    def test_email_property_has_given_value(self):
        """Test the email property has the given value."""
        assert self.event.email == "test@example.com"

    def test_to_dict_returns_expected_dict(self):
        """Test the to_dict method returns the expected dict."""
        actual = self.event.to_dict()

        assert type(actual["event_id"]) is str
        event_id = uuid.UUID(actual["event_id"])
        assert event_id.version == 7

        assert type(actual["occurred_at"]) is str
        occurred_at = datetime.fromisoformat(actual["occurred_at"])
        assert "T" in actual["occurred_at"]
        assert occurred_at.timestamp() == self.event.occurred_at.timestamp()

        assert actual["account_id"] == "account-id"
        assert actual["email"] == "test@example.com"

    def test_from_dict_returns_expected_event(self):
        """Test the from_dict method returns the expected event."""
        event_id = uuid.uuid7()
        occurred_at = datetime.now(UTC)
        actual = AccountCreatedEvent.from_dict(
            {
                "event_id": str(event_id),
                "occurred_at": occurred_at.isoformat(),
                "account_id": "account-id",
                "email": "test@example.com",
            }
        )

        assert isinstance(actual, AccountCreatedEvent)
        assert actual.event_id == event_id
        assert actual.occurred_at == occurred_at
        assert actual.account_id == "account-id"
        assert actual.email == "test@example.com"
