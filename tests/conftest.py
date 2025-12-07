"""Shared pytest fixtures for all tests."""

import pytest


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Configure anyio backend for async tests."""
    return "asyncio"


# Add your shared fixtures here as you progress through the modules.
# Examples:
#
# @pytest.fixture
# def db_session():
#     """Database session with automatic rollback."""
#     pass
#
# @pytest.fixture
# def user_factory():
#     """Factory for creating test users."""
#     pass
