# Comparaison PHP vs Python

Ce document résume les différences clés entre PHP et Python pour faciliter ta transition.

---

## Architecture Serveur

| Aspect | PHP (traditionnel) | Python (moderne) |
|--------|-------------------|------------------|
| **Process model** | Process par requête | Long-running process |
| **Bootstrap** | Chaque requête (10-50ms) | Une fois au démarrage (<1ms/req) |
| **Memory** | Isolée par requête | Partagée (attention thread-safety) |
| **Connection pool** | ❌ Re-connexion chaque fois | ✅ Pool persistent |
| **Cache in-memory** | ❌ Redis obligatoire | ✅ Simple dict Python |
| **State management** | ❌ Difficile (sessions) | ✅ Variables process (avec care) |

### Impact pratique

```python
# Python - Cache in-memory trivial
cache = {}  # Variable module, persiste entre requêtes

@app.get("/data/{id}")
def get_data(id: int):
    if id in cache:
        return cache[id]  # Instantané
    data = db.query(id)
    cache[id] = data
    return data

# PHP - Cache nécessite Redis/Memcached pour TOUT
```

---

## Concurrence

| Aspect | PHP | Python |
|--------|-----|--------|
| **WebSockets** | ❌ Swoole/ReactPHP (non-standard) | ✅ Asyncio natif |
| **SSE** | ❌ Difficile/impossible | ✅ StreamingResponse natif |
| **Long-polling** | ❌ Bloque process | ✅ async/await |
| **Async I/O** | ❌ Extensions (Amp, ReactPHP) | ✅ asyncio standard library |
| **Threading CPU** | ❌ N/A | ⚠️ GIL (limité, mais multiprocessing OK) |

### Exemple WebSocket

```python
# Python - Simple et natif
@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await broadcast_to_all(message)

# PHP - Nécessite Swoole ou ReactPHP (non-standard)
```

---

## Threading & Concurrence

| Type | PHP | Python | Use Case |
|------|-----|--------|----------|
| **Synchrone** | ✅ Standard | ✅ Standard | Requêtes simples |
| **Threading** | ❌ N/A | ⚠️ GIL (I/O OK, CPU limité) | I/O concurrent legacy |
| **Asyncio** | ❌ ReactPHP (complexe) | ✅ Natif (simple) | I/O concurrent moderne |
| **Multiprocessing** | ✅ PHP-FPM (natif) | ✅ multiprocessing module | CPU-bound tasks |

### Règle d'or Python

- **I/O-bound** (DB, API, files) → `asyncio`
- **CPU-bound** (calculs, processing) → `multiprocessing`
- **GIL** limite seulement threading CPU, pas asyncio

---

## Écosystème

| Domaine | PHP | Python |
|---------|-----|--------|
| **Web frameworks** | ✅ Laravel, Symfony | ✅ FastAPI, Django |
| **Task queues** | ⚠️ Laravel Queues, Symfony Messenger | ✅ Celery |
| **ORM** | ✅ Doctrine | ✅ SQLAlchemy |
| **Testing** | ✅ PHPUnit | ✅ pytest |
| **Migrations** | ✅ Doctrine Migrations | ✅ Alembic |
| **HTTP Client** | ✅ Guzzle | ✅ httpx, requests |
| **Validation** | ✅ Symfony Validator | ✅ Pydantic |
| **ML/AI** | ❌ Quasi-inexistant | ✅ TensorFlow, PyTorch |
| **Data Science** | ❌ Faible | ✅ pandas, NumPy |

---

## Syntaxe - Équivalences

### Naming conventions

| Élément | PHP | Python |
|---------|-----|--------|
| Variables | `$camelCase` | `snake_case` |
| Fonctions | `camelCase()` | `snake_case()` |
| Classes | `PascalCase` | `PascalCase` |
| Constantes | `UPPER_CASE` | `UPPER_CASE` |
| Méthodes privées | `private function` | `_underscore_prefix` |

### Structures

```php
// PHP
class UserService {
    private UserRepository $repository;

    public function __construct(UserRepository $repository) {
        $this->repository = $repository;
    }

    public function findById(int $id): ?User {
        return $this->repository->find($id);
    }
}
```

```python
# Python
class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def find_by_id(self, user_id: int) -> User | None:
        return self._repository.find(user_id)
```

### Null handling

```php
// PHP
$value = $user->getName() ?? 'default';
$user?->getAddress()?->getCity();
```

```python
# Python
value = user.name if user.name else 'default'
# Ou avec walrus operator
value = user.name or 'default'

# Pas d'équivalent direct au nullsafe operator
# Il faut vérifier explicitement
city = user.address.city if user and user.address else None
```

### Collections

```php
// PHP
$filtered = array_filter($items, fn($item) => $item->isActive());
$mapped = array_map(fn($item) => $item->name, $items);
```

```python
# Python - Comprehensions (plus idiomatique)
filtered = [item for item in items if item.is_active]
mapped = [item.name for item in items]

# Ou avec filter/map (moins courant)
filtered = list(filter(lambda item: item.is_active, items))
mapped = list(map(lambda item: item.name, items))
```

---

## Dependency Injection

### PHP (Symfony)

```php
// services.yaml
services:
    App\Service\UserService:
        arguments:
            - '@App\Repository\UserRepository'
```

### Python (FastAPI)

```python
# Avec Depends
from fastapi import Depends

def get_repository() -> UserRepository:
    return UserRepository(db_session)

def get_user_service(
    repository: UserRepository = Depends(get_repository)
) -> UserService:
    return UserService(repository)

@app.get("/users/{id}")
def get_user(
    id: int,
    service: UserService = Depends(get_user_service)
):
    return service.find_by_id(id)
```

---

## Testing - Équivalences

| Concept | PHPUnit | pytest |
|---------|---------|--------|
| Test method | `public function testXxx()` | `def test_xxx():` |
| Setup | `setUp()` | `@pytest.fixture` |
| Assertions | `$this->assertEquals()` | `assert x == y` |
| Mocking | `$this->createMock()` | `unittest.mock.Mock()` |
| Data providers | `@dataProvider` | `@pytest.mark.parametrize` |

### Exemple comparatif

```php
// PHPUnit
class UserServiceTest extends TestCase {
    private UserService $service;

    protected function setUp(): void {
        $this->service = new UserService(
            $this->createMock(UserRepository::class)
        );
    }

    public function testFindByIdReturnsUser(): void {
        $user = $this->service->findById(1);
        $this->assertNotNull($user);
    }
}
```

```python
# pytest
import pytest
from unittest.mock import Mock

@pytest.fixture
def user_service():
    repository = Mock(spec=UserRepository)
    return UserService(repository)

def test_find_by_id_returns_user(user_service):
    user = user_service.find_by_id(1)
    assert user is not None
```

---

## Résumé des gains Python

| Aspect | Avantage Python |
|--------|-----------------|
| **Performance I/O** | asyncio natif = gestion facile de milliers de connexions |
| **WebSockets/SSE** | Support natif, pas besoin d'extensions |
| **Setup** | UV + pyproject.toml = workflow moderne |
| **Testing** | pytest plus simple et expressif |
| **Type hints** | Similaire à PHP 8+, bien intégré |
| **Écosystème ML/Data** | Inégalé |

## Points d'attention Python

| Aspect | Vigilance requise |
|--------|-------------------|
| **GIL** | Threading CPU limité → utiliser multiprocessing |
| **Long-running** | Risque de memory leaks, restart workers |
| **État partagé** | Variables globales persistent entre requêtes |
| **Async everywhere** | Une fois async, tout doit être async |
