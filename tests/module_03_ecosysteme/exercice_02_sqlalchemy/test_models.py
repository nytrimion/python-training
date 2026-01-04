"""
Tests for SQLAlchemy models.

This demonstrates:
- Testing model creation and persistence
- Testing relationships
- Using factory fixtures
"""

from sqlalchemy.orm import Session

from src.module_03_ecosysteme.exercice_02_sqlalchemy.models import Comment, Post, User


class TestUser:
    """Tests for User model."""

    def test_create_user(self, db_session: Session, unique_email: str) -> None:
        """Test basic user creation and persistence."""
        user = User(
            email=unique_email,
            name="Alice",
        )
        db_session.add(user)
        db_session.flush()

        assert user.id is not None
        assert user.email == unique_email
        assert user.created_at is not None

    def test_user_with_bio(self, db_session: Session, unique_email: str) -> None:
        """Test user with optional bio field."""
        user = User(
            email=unique_email,
            name="Bob",
            bio="Python enthusiast",
        )
        db_session.add(user)
        db_session.flush()

        assert user.bio == "Python enthusiast"

    def test_user_without_bio(self, db_session: Session, unique_email: str) -> None:
        """Test that bio defaults to None."""
        user = User(
            email=unique_email,
            name="Charlie",
        )
        db_session.add(user)
        db_session.flush()

        assert user.bio is None


class TestPost:
    """Tests for Post model."""

    def test_create_post(self, db_session: Session, user_factory) -> None:
        """Test basic post creation with author."""
        author = user_factory(name="Alice")

        post = Post(
            title="My First Post",
            content="Hello, World!",
            author=author,
        )
        db_session.add(post)
        db_session.flush()

        assert post.id is not None
        assert post.author_id == author.id
        assert post.published is False  # Default value

    def test_post_author_relationship(self, db_session: Session, user_factory) -> None:
        """Test that post.author returns the correct user."""
        author = user_factory(name="Bob")
        post = Post(
            title="Test",
            content="Content",
            author=author,
        )
        db_session.add(post)
        db_session.flush()

        # Access relationship
        assert post.author.name == "Bob"

    def test_user_posts_relationship(self, db_session: Session, user_factory) -> None:
        """Test that user.posts returns all posts by that user."""
        author = user_factory(name="Author")

        posts: list[Post] = [
            Post(title="Post 1", content="Content", author=author),
            Post(title="Post 2", content="Content", author=author),
            Post(title="Post 3", content="Content", author=author),
        ]
        for post in posts:
            db_session.add(post)
        db_session.flush()

        assert len(author.posts) == 3
        for post in posts:
            assert post in author.posts


class TestComment:
    """Tests for Comment model."""

    def test_create_comment(
        self,
        db_session: Session,
        user_factory,
        post_factory,
    ) -> None:
        """Test comment creation with post and author."""
        author = user_factory(name="Alice")
        commenter = user_factory(name="Bob")
        post = post_factory(author=author, title="Discussion")

        comment = Comment(
            content="Great post!",
            post=post,
            author=commenter,
        )
        db_session.add(comment)
        db_session.flush()

        assert comment.id is not None
        assert comment.post_id == post.id
        assert comment.author_id == commenter.id

    def test_post_comments_relationship(
        self,
        db_session: Session,
        user_factory,
        post_factory,
    ) -> None:
        """Test that post.comments returns all comments on that post."""
        post = post_factory(author=user_factory(), title="Post")
        commenter1 = user_factory(name="Alice")
        commenter2 = user_factory(name="Bob")

        comments1: list[Comment] = [
            Comment(content="Alice's comment 1", post=post, author=commenter1),
            Comment(content="Alice's comment 2", post=post, author=commenter1),
        ]
        comments2: list[Comment] = [
            Comment(content="Bob's comment 1", post=post, author=commenter2),
            Comment(content="Bob's comment 2", post=post, author=commenter2),
        ]
        for comment in [*comments1, *comments2]:
            db_session.add(comment)
        db_session.flush()

        assert len(post.comments) == 4
        for comment in comments1:
            assert comment in post.comments
            assert comment.author is commenter1
        for comment in comments2:
            assert comment in post.comments
            assert comment.author is commenter2


class TestCascadeDelete:
    """Tests for cascade delete behavior."""

    def test_delete_user_deletes_posts(
        self,
        db_session: Session,
        user_factory,
        post_factory,
    ) -> None:
        """Test that deleting a user also deletes their posts."""
        author = user_factory(name="Alice")
        post1 = post_factory(author=author, title="Post 1")
        post2 = post_factory(author=author, title="Post 2")

        post1_id = post1.id
        post2_id = post2.id

        # Delete the user
        db_session.delete(author)
        db_session.flush()

        # Posts should be deleted (cascade)
        assert db_session.get(Post, post1_id) is None
        assert db_session.get(Post, post2_id) is None

    def test_delete_post_deletes_comments(
        self,
        db_session: Session,
        user_factory,
        post_factory,
        comment_factory,
    ) -> None:
        """Test that deleting a post also deletes its comments."""
        post = post_factory(author=user_factory())
        comment1 = comment_factory(post=post, author=user_factory())
        comment2 = comment_factory(post=post, author=user_factory())
        comment1_id = comment1.id
        comment2_id = comment2.id

        db_session.delete(post)
        db_session.flush()

        assert db_session.get(Comment, comment1_id) is None
        assert db_session.get(Comment, comment2_id) is None
