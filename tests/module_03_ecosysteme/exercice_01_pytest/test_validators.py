"""
Tests for validators module.

This file demonstrates:
- pytest.mark.parametrize for data-driven tests
- Testing pure functions (no fixtures needed)
"""

import pytest

from src.module_03_ecosysteme.exercice_01_pytest.validators import (
    validate_email,
    validate_name,
)


class TestValidateEmail:
    """Tests for email validation."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@example.com", id="simple_valid"),
            pytest.param("user.name@example.com", id="with_dot"),
            pytest.param("user+tag@example.com", id="with_plus"),
            pytest.param("user@sub.example.com", id="subdomain"),
        ],
    )
    def test_valid_emails(self, email: str) -> None:
        """Test that valid email formats are accepted."""
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("invalid", id="missing_at"),
            pytest.param("user@", id="missing_domain"),
            pytest.param("@example.com", id="missing_local"),
            pytest.param("user@domain", id="missing_tld"),
            pytest.param("", id="empty"),
            pytest.param(None, id="none"),
        ],
    )
    def test_invalid_emails(self, email: str | None) -> None:
        """Test that invalid email formats are rejected."""
        assert validate_email(email) is False


class TestValidateName:
    """Tests for name validation."""

    def test_valid_name(self) -> None:
        """Test valid name."""
        assert validate_name("Alice") is True

    def test_empty_name(self) -> None:
        """Test empty name is rejected."""
        assert validate_name("") is False

    def test_name_too_short(self) -> None:
        """Test name below minimum length."""
        assert validate_name("A") is False

    # TODO(human): Add test for custom min/max length
    # The validate_name function accepts min_length and max_length parameters
    # Write a test that verifies:
    # - A 5-character name is valid with default settings
    # - A 5-character name is invalid with min_length=10
    # - A 5-character name is invalid with max_length=3

    def test_name_length_boundaries(self) -> None:
        """Test name validation with custom length boundaries."""
        assert validate_name("Alice") is True
        assert validate_name("Alice", min_length=10) is False
        assert validate_name("Alice", max_length=3) is False
