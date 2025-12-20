"""
Shared fixtures for SQLAlchemy tests.

This demonstrates:
- Session-scoped engine (shared across all tests)
- Function-scoped session with rollback (isolation)
- Factory fixtures for creating test entities
"""

import uuid
from collections.abc import Generator
from typing import Protocol

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.module_03_ecosysteme.exercice_02_sqlalchemy.models import Base, User, Post, Comment


def _generate_unique_email() -> str:
    """Generate a unique email for testing (internal helper)."""
    return f"user-{uuid.uuid4().hex[:8]}@test.com"


@pytest.fixture(scope="session")
def engine() -> Engine:
    """
    Create engine shared across all tests in the session.

    Using a separate test database or schema would be ideal in production.
    """
    return create_engine(
        "postgresql://training:training@localhost:5432/training",
        echo=False,
    )


@pytest.fixture(scope="session")
def tables(engine: Engine) -> Generator[None, None, None]:
    """
    Create all tables before tests, drop them first for clean state.

    This runs once per test session.
    """
    # Drop first for robustness (in case previous run crashed)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    # Don't drop after - allows inspection if needed


@pytest.fixture(scope="function")
def db_session(engine: Engine, tables: None) -> Generator[Session, None, None]:
    """
    Create a new session for each test with automatic rollback.

    This ensures test isolation - each test sees a clean database state.
    """
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def unique_email() -> str:
    """Generate a unique email for each test."""
    return _generate_unique_email()


class UserFactory(Protocol):
    def __call__(
            self,
            email: str | None = None,
            name: str = "Test User",
            bio: str | None = None,
    ) -> User: ...


@pytest.fixture
def user_factory(db_session: Session) -> UserFactory:
    """
    Factory fixture for creating User entities.

    Usage:
        user = user_factory(name="Alice")
        user = user_factory(email="custom@test.com", name="Bob")
    """

    def create_user(
            email: str | None = None,
            name: str = "Test User",
            bio: str | None = None,
    ) -> User:
        if email is None:
            email = _generate_unique_email()

        user = User(
            email=email,
            name=name,
            bio=bio,
        )
        db_session.add(user)
        db_session.flush()  # Get the ID without committing
        return user

    return create_user


class PostFactory(Protocol):
    def __call__(
            self,
            author: User,
            title: str = "Test Post",
            content: str = "Test content",
            published: bool = False,
    ) -> Post: ...


@pytest.fixture
def post_factory(db_session: Session) -> PostFactory:
    """Factory fixture for creating Post entities."""

    def create_post(
            author: User,
            title: str = "Test Post",
            content: str = "Test content",
            published: bool = False,
    ) -> Post:
        post = Post(
            author=author,
            title=title,
            content=content,
            published=published,
        )
        db_session.add(post)
        db_session.flush()
        return post

    return create_post


class CommentFactory(Protocol):
    def __call__(
            self,
            post: Post,
            author: User,
            content: str = "Test content",
    ) -> Comment: ...


@pytest.fixture
def comment_factory(db_session: Session) -> CommentFactory:
    """Factory fixture for creating Comment entities."""

    def create_comment(
            post: Post,
            author: User,
            content: str = "Test content",
    ) -> Comment:
        comment = Comment(
            post=post,
            author=author,
            content=content,
        )
        db_session.add(comment)
        db_session.flush()
        return comment

    return create_comment
