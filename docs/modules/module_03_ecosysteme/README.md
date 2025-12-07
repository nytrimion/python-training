# Module 3 : Écosystème Production

## Prérequis
- Modules 1 et 2 complétés
- Compréhension d'asyncio et des long-running processes

## Objectifs d'apprentissage

À la fin de ce module, tu seras capable de :
- [ ] Configurer Celery avec Redis comme broker
- [ ] Définir et exécuter des tâches asynchrones
- [ ] Implémenter retry et error handling
- [ ] Modéliser avec SQLAlchemy ORM
- [ ] Gérer les migrations avec Alembic
- [ ] Écrire des tests avec pytest
- [ ] Utiliser fixtures et mocking

---

## Contenu

### 1. Celery - Task Queue

#### Concept
Celery permet d'exécuter des tâches en arrière-plan, de manière distribuée et fiable.

```
[FastAPI] → [Redis/RabbitMQ] → [Celery Worker]
  (API)        (Broker)         (Exécution)
```

#### Configuration de base

```python
# celery_app.py
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=True,
)
```

#### Définir une tâche

```python
@celery_app.task(bind=True, max_retries=3)
def send_email(self, to: str, subject: str, body: str) -> dict:
    """Envoie un email avec retry automatique."""
    try:
        result = email_client.send(to, subject, body)
        return {"status": "sent", "message_id": result.id}
    except EmailError as exc:
        # Retry avec backoff exponentiel
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

#### Appeler une tâche

```python
# Fire and forget
send_email.delay("user@example.com", "Welcome", "Hello!")

# Avec options
send_email.apply_async(
    args=["user@example.com", "Welcome", "Hello!"],
    countdown=60,  # Exécuter dans 60 secondes
    expires=3600,  # Expire après 1 heure
)

# Attendre le résultat (sync)
result = send_email.delay("user@example.com", "Welcome", "Hello!")
result.get(timeout=10)  # Bloque jusqu'au résultat
```

#### Lancer le worker

```bash
celery -A celery_app worker --loglevel=info
```

---

### 2. SQLAlchemy - ORM

#### Analogie PHP
```
Doctrine ORM  ↔  SQLAlchemy ORM
Doctrine DBAL ↔  SQLAlchemy Core
Migrations    ↔  Alembic
```

#### Définir un modèle

```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relation one-to-many
    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="posts")
```

#### Sessions et transactions

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(bind=engine)

# Context manager recommandé
with SessionLocal() as session:
    user = User(email="alice@example.com", name="Alice")
    session.add(user)
    session.commit()
    session.refresh(user)
    print(user.id)
```

#### Queries

```python
from sqlalchemy import select

with SessionLocal() as session:
    # Get by ID
    user = session.get(User, 1)

    # Query avec filtre
    stmt = select(User).where(User.email == "alice@example.com")
    user = session.execute(stmt).scalar_one_or_none()

    # Query avec join
    stmt = (
        select(Post)
        .join(User)
        .where(User.name == "Alice")
        .order_by(Post.created_at.desc())
        .limit(10)
    )
    posts = session.execute(stmt).scalars().all()
```

---

### 3. Alembic - Migrations

#### Initialisation

```bash
# Créer la structure Alembic
alembic init alembic

# Configurer alembic.ini
sqlalchemy.url = postgresql://user:pass@localhost/db
```

#### Créer une migration

```bash
# Auto-génère depuis les modèles
alembic revision --autogenerate -m "create users table"

# Migration manuelle
alembic revision -m "add index on email"
```

#### Appliquer les migrations

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1

# Voir l'historique
alembic history
```

---

### 4. pytest - Testing

#### Structure de base

```python
# tests/test_user.py
import pytest
from app.models import User

def test_user_creation():
    """Test simple sans fixture."""
    user = User(email="test@example.com", name="Test")
    assert user.email == "test@example.com"
    assert user.name == "Test"


class TestUserService:
    """Grouper les tests par domaine."""

    def test_get_user_by_email(self, user_service):
        user = user_service.get_by_email("alice@example.com")
        assert user is not None
        assert user.name == "Alice"

    def test_user_not_found(self, user_service):
        user = user_service.get_by_email("unknown@example.com")
        assert user is None
```

#### Fixtures

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    """Engine partagé pour tous les tests."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function")
def db_session(engine):
    """Session avec rollback après chaque test."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()


@pytest.fixture
def user_factory(db_session):
    """Factory pour créer des users de test."""
    def create_user(email: str = "test@example.com", name: str = "Test"):
        user = User(email=email, name=name)
        db_session.add(user)
        db_session.commit()
        return user
    return create_user
```

#### Mocking

```python
from unittest.mock import Mock, patch, AsyncMock

def test_send_email_success(user_service):
    """Mock du client email."""
    with patch.object(user_service, "email_client") as mock_client:
        mock_client.send.return_value = {"id": "123"}

        result = user_service.send_welcome_email("alice@example.com")

        mock_client.send.assert_called_once()
        assert result["id"] == "123"


@pytest.mark.asyncio
async def test_async_fetch():
    """Mock d'une fonction async."""
    with patch("app.client.fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"data": "test"}

        result = await fetch_user_data(1)

        assert result["data"] == "test"
```

#### Parametrized tests

```python
@pytest.mark.parametrize("email,expected_valid", [
    ("valid@example.com", True),
    ("invalid", False),
    ("no@domain", False),
    ("user@domain.com", True),
])
def test_email_validation(email: str, expected_valid: bool):
    result = validate_email(email)
    assert result == expected_valid
```

---

## Exercices

### Exercice 1 : Celery Tasks

Configure Celery et implémente :
1. Une tâche `send_notification` avec retry
2. Une tâche `process_image` (simulée)
3. Une chain de tâches

→ Fichier : `src/module_03_ecosysteme/exercice_01_celery/`

### Exercice 2 : SQLAlchemy Models

Modélise un domaine simple avec :
1. `User` (id, email, name)
2. `Post` (id, title, content, author_id)
3. `Comment` (id, content, post_id, author_id)

Implémente les relations et quelques queries.

→ Fichier : `src/module_03_ecosysteme/exercice_02_sqlalchemy/`

### Exercice 3 : Tests avec pytest

Écris des tests pour :
1. Le modèle User (création, validation)
2. Un service UserService (avec mocking)
3. Tests paramétrés pour la validation

→ Fichier : `src/module_03_ecosysteme/exercice_03_pytest/`

---

## Checkpoint

Avant de passer au module suivant, assure-toi de pouvoir répondre à :

1. **Celery** : Quelle est la différence entre `.delay()` et `.apply_async()` ?
2. **Celery** : Comment implémenter un retry avec backoff exponentiel ?
3. **SQLAlchemy** : Comment éviter les N+1 queries avec les relations ?
4. **pytest** : Quelle est la différence entre `scope="function"` et `scope="session"` ?
