# Formation Python - Transition PHP → Python
**Durée :** 1 mois (avant intégration Dailymotion)
**Charge :** ~40h total (1h/jour en moyenne)
**Objectif :** Maîtriser spécificités Python + écosystème moderne

---

## 🎯 Ce que tu maîtrises déjà (transférable)

### Architecture & Patterns ✅
- DDD (Domain-Driven Design)
- Clean Architecture (séparation couches)
- SOLID principles
- CQRS (Command Query Responsibility Segregation)
- Event-driven architecture
- Design patterns GoF

**→ Ces compétences sont language-agnostic**
**→ Elles s'appliquent directement en Python**
**→ Ton test technique l'a prouvé**

---

## 🔍 Ce qui manque (apprentissage Python-specific)

### Connaissances à acquérir
1. **GIL** (Global Interpreter Lock) et ses implications
2. **Asyncio** (event loop, concurrent I/O)
3. **Long-running processes** (vs PHP process-per-request)
4. **WebSockets natifs** (vs PHP/Swoole)
5. **Écosystème** (Celery, FastAPI, SQLAlchemy, pytest)

**→ Ce n'est PAS une refonte totale**
**→ C'est appliquer ton expertise avec de nouveaux outils**

---

## 📚 Roadmap Formation 4 Semaines

### 📅 Semaine 1 : Fondations Python + Particularités

#### Priorité 1 : GIL et Threading Model (2-3h)
**Ressources :**
- Article : "Understanding the Python GIL" (Real Python)
- https://realpython.com/python-gil/

**À comprendre :**
- Qu'est-ce que le GIL ?
- Pourquoi Python limite le threading CPU
- Différences threading / asyncio / multiprocessing
- Quand utiliser chaque approche

**Exercice pratique :**
```python
# Expérimente ces 3 approches sur une tâche I/O-bound
import threading
import asyncio
import multiprocessing

# Compare les performances
```

---

#### Priorité 2 : Long-running Processes vs PHP (2h)
**Ressources :**
- Doc : Gunicorn / Uvicorn architecture
- Article : "How Python Web Servers Work"

**À comprendre :**
- Différence fondamentale PHP (process-per-request) vs Python (long-running)
- Application lifecycle (startup une fois, sert N requêtes)
- Implications : cache in-memory, connection pooling, shared state
- Trade-offs : memory leaks potentiels, restart strategies

**Comparaison clé :**
```
PHP (chaque requête) :
1. Bootstrap framework (10-50ms)
2. Connexion DB
3. Traite requête
4. Ferme tout
5. Process meurt

Python (long-running) :
1. Bootstrap framework (une fois au démarrage)
2. Connection pool DB (persistent)
3. Traite requête N fois (réutilise tout)

→ 10-50× plus rapide pour requêtes légères
```

---

#### Priorité 3 : Syntaxe et Idiomes Python (4-5h)
**Ressources :**
- PEP8 Style Guide
- Tutorial : "Python for Experienced Developers"
- Doc : Type hints (PEP 484)

**À maîtriser :**
- PEP8 conventions (naming, formatting)
- Type hints (`def func(x: int) -> str:`)
- Decorators (`@property`, `@staticmethod`, custom)
- Context managers (`with` statement)
- List/dict comprehensions
- Generators et `yield`

**Exercice pratique :**
```python
# Réécris une classe PHP en Python idiomatique
# Applique type hints, decorators, comprehensions
```

**Total Semaine 1 : ~10h**

---

### 📅 Semaine 2 : Asyncio Profond

#### Priorité 1 : Asyncio Event Loop (4-5h)
**Ressources :**
- Tutorial : "AsyncIO in Python: A Complete Walkthrough" (Real Python)
- https://realpython.com/async-io-python/
- Doc officielle : https://docs.python.org/3/library/asyncio.html

**À maîtriser :**
- Event loop : comment ça fonctionne
- `async def` vs `def`
- `await` keyword (quand et pourquoi)
- Tasks vs coroutines
- Concurrency vs parallelism (important !)
- `asyncio.create_task()`, `asyncio.gather()`

**Exercice pratique :**
```python
# Implémente 3 scenarios :
# 1. Sync (baseline)
# 2. Threading (I/O-bound)
# 3. Asyncio (I/O-bound)
# Compare performances et complexité
```

---

#### Priorité 2 : FastAPI Async Patterns (3h)
**Ressources :**
- Doc FastAPI : https://fastapi.tiangolo.com/async/
- Tutorial : FastAPI Background Tasks

**À maîtriser :**
- Endpoints async vs sync (quand utiliser chaque)
- Background tasks (pour ton use case events)
- Dependency injection FastAPI
- Async database access (avec SQLAlchemy)

**Exercice pratique :**
```python
# Reprends ton test technique
# Implémente EventDispatcher avec FastAPI BackgroundTasks
```

---

#### Priorité 3 : WebSockets Natifs (2h)
**Ressources :**
- Tutorial : "WebSockets with FastAPI"
- https://fastapi.tiangolo.com/advanced/websockets/

**À comprendre :**
- Différence avec PHP (natif vs Swoole/ReactPHP)
- SSE (Server-Sent Events)
- Long-polling patterns

**Exercice pratique :**
```python
# Mini-chat temps réel avec WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Implémente broadcast basique
```

**Total Semaine 2 : ~10h**

---

### 📅 Semaine 3 : Écosystème Production

#### Priorité 1 : Celery Task Queues (4h)
**Ressources :**
- Tutorial : "First Steps with Celery"
- https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html
- Doc : Redis/RabbitMQ brokers

**À maîtriser :**
- Architecture Celery (broker, workers, result backend)
- Définir tasks (`@celery_app.task`)
- Enqueue tasks (`.delay()`, `.apply_async()`)
- Retry automatique (`max_retries`, `countdown`)
- Monitoring avec Flower

**Exercice pratique :**
```python
# Reprends ton test technique
# Implémente EventDispatcher avec Celery
# Configure Redis comme broker
# Lance worker
# Teste retry sur failure

# Compare avec FastAPI BackgroundTasks
```

---

#### Priorité 2 : ORMs Python - SQLAlchemy (3h)
**Ressources :**
- Tutorial : SQLAlchemy Core + ORM
- https://docs.sqlalchemy.org/en/20/tutorial/
- Doc : Alembic (migrations)

**À comprendre :**
- SQLAlchemy Core vs ORM (équivalent Doctrine DBAL vs ORM)
- Sessions et transactions
- Relationships (one-to-many, many-to-many)
- Migrations avec Alembic
- Async support (SQLAlchemy 2.0+)

**Exercice pratique :**
```python
# Modélise ton domain du test technique avec SQLAlchemy
# Configure Alembic
# Crée migrations
```

---

#### Priorité 3 : Testing Python (3h)
**Ressources :**
- Doc pytest : https://docs.pytest.org/
- Tutorial : "Effective Python Testing With Pytest"

**À maîtriser :**
- pytest basics (`assert`, fixtures)
- Mocking (`unittest.mock`, `pytest-mock`)
- Parametrized tests
- Async testing (`pytest-asyncio`)
- Coverage (`pytest-cov`)

**Exercice pratique :**
```python
# Teste ton EventDispatcher (3 implémentations)
# Tests unitaires + tests d'intégration
# Vise >80% coverage
```

**Total Semaine 3 : ~10h**

---

### 📅 Semaine 4 : Projet Intégrateur + Agents IA

#### Priorité 1 : Mini-projet DDD Python (6h)
**Objectif :** Synthétiser tout ce que tu as appris

**Projet :**
```python
# Reprends ton test technique complet
# Implémente 3 versions EventDispatcher :

# 1. SyncEventDispatcher (baseline)
class SyncEventDispatcher(EventDispatcher):
    def dispatch(self, event):
        handler.handle(event)  # Bloquant

# 2. AsyncioEventDispatcher (générique, MVP)
class AsyncioEventDispatcher(EventDispatcher):
    def dispatch(self, event):
        asyncio.create_task(handler.handle(event))

# 3. CeleryEventDispatcher (production robuste)
class CeleryEventDispatcher(EventDispatcher):
    def dispatch(self, event):
        process_event.delay(event.to_dict())

# Compare :
# - Performance (temps réponse API)
# - Complexité implémentation
# - Garanties (delivery, retry)
# - Généricité (HTTP, CLI, batch)
```

**Livrables :**
- Code complet avec 3 implémentations
- Tests pour chaque
- README comparatif (trade-offs)
- Benchmarks performance

---

#### Priorité 2 : Agents IA Avancés (4h)
**Ressources :**
- Doc : Claude MCP servers
- https://docs.anthropic.com/en/docs/build-with-claude/mcp

**À explorer :**
- MCP servers configuration
- Custom prompts Python-specific (ex: "Always use type hints")
- Sous-agents spécialisés :
  - Code review agent (avec guidelines Dailymotion si dispos)
  - Test generation agent
  - Documentation agent

**Exercice pratique :**
```
Configure 2-3 sous-agents dans Claude Code
Teste-les sur ton mini-projet
Documente workflow pour partage équipe
```

**Total Semaine 4 : ~10h**

---

## 📊 Différences Clés PHP vs Python

### Architecture Serveur

| Aspect | PHP (traditionnel) | Python (moderne) |
|--------|-------------------|------------------|
| **Process model** | Process par requête | Long-running process |
| **Bootstrap** | Chaque requête (10-50ms) | Une fois au démarrage (<1ms/req) |
| **Memory** | Isolée par requête | Partagée (attention thread-safety) |
| **Connection pool** | ❌ Re-connexion chaque fois | ✅ Pool persistent |
| **Cache in-memory** | ❌ Redis obligatoire | ✅ Simple dict Python |
| **State management** | ❌ Difficile (sessions) | ✅ Variables process (avec care) |

**Impact pratique :**
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

### Concurrence

| Aspect | PHP | Python |
|--------|-----|--------|
| **WebSockets** | ❌ Swoole/ReactPHP (non-standard) | ✅ Asyncio natif (10 lignes) |
| **SSE** | ❌ Difficile/impossible | ✅ StreamingResponse natif |
| **Long-polling** | ❌ Bloque process | ✅ async/await |
| **Async I/O** | ❌ Extensions (Amp, ReactPHP) | ✅ asyncio standard library |
| **Threading CPU** | ❌ N/A | ⚠️ GIL (limité, mais multiprocessing OK) |

**Exemple WebSocket (impossible en PHP standard) :**
```python
@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await broadcast_to_all(message)  # Temps réel
```

---

### Threading & Concurrence

| Type | PHP | Python | Use Case |
|------|-----|--------|----------|
| **Synchrone** | ✅ Standard | ✅ Standard | Requêtes simples |
| **Threading** | ❌ N/A | ⚠️ GIL (I/O OK, CPU limité) | I/O concurrent legacy |
| **Asyncio** | ❌ ReactPHP (complexe) | ✅ Natif (simple) | I/O concurrent moderne |
| **Multiprocessing** | ✅ PHP-FPM (natif) | ✅ multiprocessing module | CPU-bound tasks |

**Règle d'or Python :**
- **I/O-bound** (DB, API, files) → asyncio
- **CPU-bound** (calculs, processing) → multiprocessing
- **GIL** limite seulement threading CPU, pas asyncio

---

### Écosystème

| Domaine | PHP | Python |
|---------|-----|--------|
| **Web frameworks** | ✅ Laravel, Symfony (excellents) | ✅ FastAPI, Django (excellents) |
| **Task queues** | ⚠️ Laravel Queues, Symfony Messenger | ✅ Celery (standard de facto) |
| **ML/AI** | ❌ Quasi-inexistant | ✅ TensorFlow, PyTorch, scikit-learn |
| **Data Science** | ❌ Faible | ✅ pandas, NumPy, Jupyter |
| **Testing** | ✅ PHPUnit (mature) | ✅ pytest (excellent) |
| **Type system** | ⚠️ Récent (7.4+), optionnel | ⚠️ Type hints optionnels aussi |

---

## 🏗️ Architecture Clean : Avantage Majeur

### Ce que tu as bien fait dans ton test

**EventDispatcher abstrait (Domain Layer) :**
```python
from abc import ABC, abstractmethod

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: DomainEvent) -> None:
        pass
```

**Command ne dépend QUE de l'abstraction :**
```python
class CreateAccountCommand:
    def __init__(self, dispatcher: EventDispatcher):
        self.dispatcher = dispatcher

    def execute(self, data):
        account = Account.create(data)
        self.dispatcher.dispatch(AccountCreatedEvent(account))
        return account
```

**→ Domain/Application layers ignorent l'infrastructure**
**→ Swappable à volonté**
**→ Testable facilement (mock dispatcher)**

---

### Les 3 implémentations (Infrastructure Layer)

#### 1. SyncEventDispatcher (MVP simple)
```python
class SyncEventDispatcher(EventDispatcher):
    def __init__(self, handlers: dict):
        self.handlers = handlers

    def dispatch(self, event: DomainEvent) -> None:
        handler = self.handlers[type(event)]
        handler.handle(event)  # Bloquant
```

**Avantages :**
- ✅ Simple (10 lignes)
- ✅ Pas de dépendance
- ✅ Debugging facile

**Inconvénients :**
- ❌ Bloque réponse API (300-500ms email)

---

#### 2. AsyncioEventDispatcher (MVP générique)
```python
import asyncio

class AsyncioEventDispatcher(EventDispatcher):
    def __init__(self, handlers: dict):
        self.handlers = handlers

    def dispatch(self, event: DomainEvent) -> None:
        handler = self.handlers[type(event)]
        asyncio.create_task(handler.handle(event))
        # Retourne immédiatement, handler exécuté en arrière-plan
```

**Avantages :**
- ✅ Non-bloquant (réponse API rapide)
- ✅ Pas de dépendance externe (Redis/Rabbit)
- ✅ Utilisable partout (HTTP, CLI, batch)
- ✅ I/O concurrent (parfait pour DB + mailer)

**Inconvénients :**
- ⚠️ Pas de garantie delivery (crash = perdu)
- ⚠️ Pas de retry automatique
- ⚠️ Difficile à monitorer

**→ Parfait pour ton use case MVP** ✅

---

#### 3. CeleryEventDispatcher (Production robuste)
```python
from celery import Celery

celery_app = Celery('app', broker='redis://localhost')

class CeleryEventDispatcher(EventDispatcher):
    def dispatch(self, event: DomainEvent) -> None:
        process_event.delay(
            event_type=type(event).__name__,
            event_data=event.to_dict()
        )

@celery_app.task(bind=True, max_retries=3)
def process_event(self, event_type: str, event_data: dict):
    try:
        event = reconstruct_event(event_type, event_data)
        handler = get_handler(event_type)
        handler.handle(event)
    except Exception as exc:
        # Retry automatique avec backoff
        raise self.retry(exc=exc, countdown=60)
```

**Avantages :**
- ✅ Garantie delivery (Redis/Rabbit persistent)
- ✅ Retry automatique (mailer API down)
- ✅ Monitoring (Flower dashboard)
- ✅ Scale horizontal (multiple workers)
- ✅ Utilisable partout (HTTP, CLI, batch)

**Inconvénients :**
- ⚠️ Infrastructure requise (Redis/Rabbit)
- ⚠️ Complexité setup

**→ Upgrade path naturel pour production** ✅

---

### Migration transparente

**L'architecture Clean permet :**

```python
# Configuration (dependency injection)

# MVP
dispatcher = AsyncioEventDispatcher(handlers)

# Production (juste swap implementation)
dispatcher = CeleryEventDispatcher(celery_app, handlers)

# Domain/Application code = INCHANGÉ ✅
command = CreateAccountCommand(dispatcher)
command.execute(data)
```

**→ C'est la force de Clean Architecture**
**→ Infrastructure swappable sans toucher business logic**
**→ Tu l'as bien appliqué dans ton test** 🎯

---

## 🎯 Ton Use Case Spécifique : AccountCreated

### Event handler détaillé

```python
class AccountCreatedHandler:
    async def handle(self, event: AccountCreatedEvent):
        # 1. Génère code (CPU léger, ~1ms)
        code = generate_verification_code()

        # 2. Save DB (I/O, ~50-100ms)
        await db.save(VerificationCode(
            account_id=event.account.id,
            code=code,
            expires_at=now() + timedelta(hours=24)
        ))

        # 3. Render HTML (CPU léger, ~10-50ms)
        html = render_template(
            "verification_email.html",
            code=code,
            account=event.account
        )

        # 4. Send email via API (I/O, ~200-500ms)
        await mailer_client.send_email(
            to=event.account.email,
            subject="Vérification de votre compte",
            html=html
        )
```

**Temps total : ~300-700ms**

**Analyse :**
- CPU-bound tasks : ~10-50ms (11-60ms total, négligeable)
- I/O-bound tasks : ~250-600ms (85-90% du temps)

**→ I/O-bound dominant = asyncio parfait** ✅
**→ GIL non-problématique (pas de CPU intensif)** ✅

---

### Pourquoi asyncio approprié ici

1. ✅ **I/O dominant** (DB + API mailer, pas calculs)
2. ✅ **Pas de GIL concern** (I/O libère GIL automatiquement)
3. ✅ **Concurrent I/O possible** (DB write + email send peuvent overlap)
4. ✅ **Générique** (HTTP, CLI, batch avec `asyncio.run()`)
5. ✅ **Pas de dépendance** (Redis/Rabbit pas nécessaire MVP)
6. ✅ **Clean Architecture respectée** (via EventDispatcher abstrait)

**→ Solution élégante et appropriée** 🎯

---

## 📝 Checklist Progression

### Semaine 1
- [ ] Comprendre GIL et implications
- [ ] Comprendre long-running processes
- [ ] Maîtriser syntaxe Python idiomatique
- [ ] Expérimenter threading vs asyncio

### Semaine 2
- [ ] Maîtriser asyncio event loop
- [ ] Comprendre async/await keywords
- [ ] Implémenter FastAPI background tasks
- [ ] Créer mini WebSocket chat

### Semaine 3
- [ ] Setup Celery + Redis
- [ ] Implémenter tasks avec retry
- [ ] Apprendre SQLAlchemy ORM
- [ ] Écrire tests pytest

### Semaine 4
- [ ] Projet intégrateur : 3 EventDispatcher implémentations
- [ ] Benchmarks comparatifs
- [ ] Configure sous-agents IA
- [ ] Documentation workflow

---

## 🚀 Après le Mois de Formation

**Tu seras prêt pour :**
- ✅ Onboarding Python chez Dailymotion
- ✅ Pair programming avec équipe
- ✅ Code reviews Python
- ✅ Contribution immédiate (architecture)
- ✅ Partage expertise IA (workshops/embedded)

**Ce qui reste à apprendre (on-the-job) :**
- Stack spécifique Dailymotion
- Guidelines équipe
- Domain métier
- Quirks production

**Mais la fondation sera solide.** ✅

---

## 💡 Ressources Complémentaires

### Livres (optionnel)
- "Fluent Python" - Luciano Ramalho (référence)
- "Python Concurrency with asyncio" - Matthew Fowler

### Sites
- Real Python (tutorials excellents)
- Python official docs (très bien écrite)
- FastAPI docs (excellent tutorial)

### Communautés
- r/Python (Reddit)
- Python Discord
- Stack Overflow (Python tag)

---

## 🎯 Objectif Final

**Devenir :**
```
Senior Backend Python
= Architecture solide (déjà acquis)
+ Syntaxe Python idiomatique (Semaine 1)
+ Asyncio mastery (Semaine 2)
+ Écosystème moderne (Semaine 3)
+ Expérience pratique (Semaine 4)
```

**Timeline réaliste :**
- **Mois 1** (pré-intégration) : Fondations solides
- **Mois 1-3** (post-intégration) : Montée en compétence progressive
- **Mois 3-6** : Autonomie Python complète
- **Mois 6-12** : Senior Python confirmé

**Tu y arriveras.** 🎯

**Tu as 23 ans d'expérience architecture.**
**Python n'est qu'une nouvelle syntaxe pour exprimer ce que tu maîtrises déjà.**
