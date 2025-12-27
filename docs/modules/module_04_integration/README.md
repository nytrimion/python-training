# Module 4 : Projet Intégrateur

## Prérequis
- Modules 1, 2 et 3 complétés
- Maîtrise d'asyncio, Celery, SQLAlchemy et pytest

## Objectif

Implémenter un système d'Event Dispatching en Clean Architecture avec **3 implémentations** interchangeables, démontrant la puissance de l'abstraction.

---

## Le Projet : EventDispatcher DDD

### Contexte métier

Tu dois implémenter un système où la création d'un compte utilisateur déclenche l'envoi d'un email de vérification.

```
[CreateAccountCommand] → [EventDispatcher] → [VerifyAccountEmailHandler]
                              ↑                        ↓
                        (abstraction)          [Verify account email]
```

### Architecture cible

```
src/module_04_integration/
├── domain/
│   ├── events.py           # DomainEvent, AccountCreatedEvent
│   └── dispatcher.py       # Interface abstraite EventDispatcher
│
├── application/
│   ├── commands.py         # CreateAccountCommand
│   └── handlers.py         # VerifyAccountEmailHandler
│
└── infrastructure/
    ├── http/                   # Driving adapter (expose l'application)
    │   └── main.py             # FastAPI endpoints
    ├── sync_dispatcher.py      # Driven adapters (implémentations)
    ├── asyncio_dispatcher.py
    └── celery_dispatcher.py
```

---

## Partie 1 : Domain Layer

### DomainEvent (base class)

```python
# domain/events.py
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class DomainEvent(ABC):
    """Base class for all domain events."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize event for queue transport."""
        raise NotImplementedError
```

### EventDispatcher (interface abstraite)

```python
# domain/dispatcher.py
from abc import ABC, abstractmethod
from .events import DomainEvent

class EventDispatcher(ABC):
    """Abstract interface for event dispatching."""

    @abstractmethod
    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event to its handlers."""
        pass
```

---

## Partie 2 : Les 3 Implémentations

### 1. SyncEventDispatcher

**Caractéristiques :**
- Exécution synchrone (bloquante)
- Simple, facile à débugger
- Pas de dépendance externe

```python
# infrastructure/sync_dispatcher.py
class SyncEventDispatcher(EventDispatcher):
    def __init__(self, handlers: dict[type, Handler]):
        self._handlers = handlers

    def dispatch(self, event: DomainEvent) -> None:
        handler = self._handlers.get(type(event))
        if handler:
            handler.handle(event)  # Bloquant
```

### 2. AsyncioEventDispatcher

**Caractéristiques :**
- Non-bloquant (fire and forget)
- Pas de garantie de delivery
- Idéal pour MVP

```python
# infrastructure/asyncio_dispatcher.py
import asyncio

class AsyncioEventDispatcher(EventDispatcher):
    def __init__(self, handlers: dict[type, Handler]):
        self._handlers = handlers

    def dispatch(self, event: DomainEvent) -> None:
        handler = self._handlers.get(type(event))
        if handler:
            asyncio.create_task(handler.handle(event))
            # Retourne immédiatement
```

### 3. CeleryEventDispatcher

**Caractéristiques :**
- Garantie de delivery (persistence)
- Retry automatique
- Monitoring (Flower)
- Scalable

```python
# infrastructure/celery_dispatcher.py
from celery import Celery

class CeleryEventDispatcher(EventDispatcher):
    def __init__(self, celery_app: Celery, handlers: dict[type, Handler]):
        self._celery_app = celery_app
        self._handlers = handlers
        self._register_tasks()

    def dispatch(self, event: DomainEvent) -> None:
        task_name = f"handle_{type(event).__name__}"
        self._celery_app.send_task(task_name, args=[event.to_dict()])
```

---

## Partie 3 : Application Layer

### Command

```python
# application/commands.py
@dataclass
class CreateAccountCommand:
    dispatcher: EventDispatcher
    repository: AccountRepository

    def execute(self, data: CreateAccountData) -> Account:
        account = Account.create(data)
        self.repository.save(account)
        self.dispatcher.dispatch(AccountCreatedEvent(account))
        return account
```

### Handler

```python
# application/handlers.py
class VerifyAccountEmailHandler:
    def __init__(self, mailer: MailerService, db: Database):
        self._mailer = mailer
        self._db = db

    async def handle(self, event: AccountCreatedEvent) -> None:
        # Generate verification code
        code = generate_code()
        await self._db.save_verification_code(event.account_id, code)

        # Send email
        await self._mailer.send(
            to=event.account_email,
            template="verification",
            context={"code": code}
        )
```

---

## Partie 4 : Tests

### Structure des tests

```
tests/module_04_integration/
├── test_sync_dispatcher.py
├── test_asyncio_dispatcher.py
├── test_celery_dispatcher.py
├── test_create_account_command.py
└── test_api_integration.py
```

### Exemple de test

```python
# test_sync_dispatcher.py
import pytest
from unittest.mock import Mock

def test_sync_dispatcher_calls_handler():
    # Arrange
    mock_handler = Mock()
    handlers = {AccountCreatedEvent: mock_handler}
    dispatcher = SyncEventDispatcher(handlers)
    event = AccountCreatedEvent(account_id="123", email="test@example.com")

    # Act
    dispatcher.dispatch(event)

    # Assert
    mock_handler.handle.assert_called_once_with(event)
```

---

## Partie 5 : Benchmarks

Crée un script de benchmark comparant les 3 implémentations :

```python
# benchmarks/compare_dispatchers.py
import time
import asyncio
from statistics import mean

def benchmark_dispatcher(dispatcher: EventDispatcher, n_events: int = 100) -> float:
    """Mesure le temps moyen pour dispatcher N events."""
    events = [AccountCreatedEvent(...) for _ in range(n_events)]

    start = time.perf_counter()
    for event in events:
        dispatcher.dispatch(event)
    elapsed = time.perf_counter() - start

    return elapsed / n_events
```

### Métriques à comparer

| Métrique | Sync | Asyncio | Celery |
|----------|------|---------|--------|
| Latence réponse API | ❌ Élevée | ✅ Faible | ✅ Faible |
| Garantie delivery | ❌ Non | ❌ Non | ✅ Oui |
| Retry automatique | ❌ Non | ❌ Non | ✅ Oui |
| Complexité setup | ✅ Simple | ✅ Simple | ⚠️ Moyenne |
| Debugging | ✅ Facile | ⚠️ Moyen | ⚠️ Moyen |

---

## Livrables attendus

1. **Code complet** avec les 3 implémentations
2. **Tests unitaires** pour chaque implémentation (coverage > 80%)
3. **Tests d'intégration** pour l'API FastAPI
4. **Benchmarks** documentés
5. **README** avec trade-offs et recommandations

---

## Étapes suggérées

1. [ ] Créer la structure de dossiers
2. [ ] Implémenter `DomainEvent` et `AccountCreatedEvent`
3. [ ] Implémenter l'interface `EventDispatcher`
4. [ ] Implémenter `SyncEventDispatcher` + tests
5. [ ] Implémenter `AsyncioEventDispatcher` + tests
6. [ ] Implémenter `CeleryEventDispatcher` + tests
7. [ ] Créer l'API FastAPI avec injection de dépendances
8. [ ] Écrire les tests d'intégration
9. [ ] Créer les benchmarks
10. [ ] Documenter les trade-offs

---

## Checkpoint Final

À la fin de ce projet, tu dois pouvoir :

1. **Expliquer** pourquoi l'abstraction `EventDispatcher` est importante
2. **Démontrer** comment swapper une implémentation sans toucher au code métier
3. **Justifier** le choix d'une implémentation selon le contexte (MVP vs production)
4. **Comparer** les performances et trade-offs de chaque approche
