"""
Shared fixtures for SQLAlchemy tests.

This demonstrates:
- Session-scoped engine (shared across all tests)
- Function-scoped session with rollback (isolation)
- Factory fixtures for creating test entities
"""

import logging
import os
import uuid
from collections.abc import Generator
from typing import Protocol

import alembic.command
import pytest
from alembic.config import Config
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

from src.module_03_ecosysteme.exercice_02_sqlalchemy.models import (
    Base,
    Comment,
    Post,
    User,
)

logger = logging.getLogger(__name__)


def _generate_unique_email() -> str:
    """Generate a unique email for testing (internal helper)."""
    return f"user-{uuid.uuid4().hex[:8]}@test.com"


def _setup_tables_via_migrations(engine: Engine) -> None:
    """
    Create all via migrations (more realistic).

    Drop them first for clean state.
    """
    logger.info("Setting up tables via Alembic migrations")
    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()
    alembic.command.upgrade(Config("alembic.ini"), "head")


def _setup_tables_via_metadata(engine: Engine) -> None:
    """
    Create all via metadata.

    Drop them first for clean state.
    """
    logger.info("Setting up tables via SQLAlchemy metadata")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


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
def _tables(engine: Engine) -> Generator[None, None, None]:
    """Setup tables once per session."""
    if os.getenv("TEST_USE_MIGRATIONS", "true").lower() == "true":
        _setup_tables_via_migrations(engine)
    else:
        _setup_tables_via_metadata(engine)
    yield


@pytest.fixture(scope="function")
def db_session(engine: Engine, _tables: None) -> Generator[Session, None, None]:
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
