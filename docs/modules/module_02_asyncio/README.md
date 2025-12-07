# Module 2 : Asyncio

## Prérequis
- Module 1 complété
- Compréhension du GIL et des long-running processes

## Objectifs d'apprentissage

À la fin de ce module, tu seras capable de :
- [ ] Expliquer le fonctionnement de l'event loop
- [ ] Distinguer coroutines, tasks et futures
- [ ] Utiliser `async def`, `await`, `asyncio.create_task()`
- [ ] Gérer la concurrence avec `asyncio.gather()`
- [ ] Implémenter des endpoints FastAPI async
- [ ] Créer un WebSocket simple

---

## Contenu

### 1. L'Event Loop - Concept Fondamental

#### Analogie
Imagine un serveur de restaurant avec un seul serveur :
- **Sync** : Le serveur attend que la cuisine prépare le plat avant de prendre la commande suivante
- **Async** : Le serveur prend plusieurs commandes, les transmet à la cuisine, et revient chercher les plats quand ils sont prêts

#### En Python

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Simule une requête HTTP async."""
    print(f"Début requête: {url}")
    await asyncio.sleep(1)  # Simule I/O (libère l'event loop)
    print(f"Fin requête: {url}")
    return {"url": url, "data": "..."}

async def main():
    # Ces 3 requêtes s'exécutent en parallèle (concurrence)
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
    )
    print(f"Résultats: {results}")

# Point d'entrée
asyncio.run(main())
```

**Temps total** : ~1 seconde (pas 3 secondes !)

---

### 2. async def vs def

```python
# Fonction synchrone classique
def sync_function() -> str:
    return "result"

# Coroutine (fonction async)
async def async_function() -> str:
    await asyncio.sleep(0.1)  # Point de suspension
    return "result"

# Appel
result = sync_function()           # Retourne directement "result"
coro = async_function()            # Retourne un objet coroutine (pas exécuté!)
result = await async_function()    # Exécute et attend le résultat
```

#### Règle d'or
- `await` ne peut être utilisé que dans une fonction `async def`
- Une fonction `async def` doit être `await`ed pour s'exécuter

---

### 3. Tasks vs Coroutines

```python
async def my_coroutine():
    await asyncio.sleep(1)
    return "done"

async def main():
    # COROUTINE: s'exécute séquentiellement
    result1 = await my_coroutine()  # Attend 1s
    result2 = await my_coroutine()  # Attend 1s de plus
    # Total: 2 secondes

    # TASK: s'exécute en parallèle (concurrence)
    task1 = asyncio.create_task(my_coroutine())
    task2 = asyncio.create_task(my_coroutine())
    result1 = await task1
    result2 = await task2
    # Total: ~1 seconde (concurrence!)
```

---

### 4. Patterns Asyncio Essentiels

#### gather - Exécuter plusieurs tâches en parallèle

```python
async def main():
    # Toutes les tâches démarrent en même temps
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    # results = [user1, user2, user3]
```

#### create_task - Fire and forget (avec précaution)

```python
async def send_email(to: str, content: str) -> None:
    await email_client.send(to, content)

async def create_account(data: dict) -> Account:
    account = Account.create(data)
    await db.save(account)

    # Envoyer email en arrière-plan (n'attend pas)
    asyncio.create_task(send_email(account.email, "Welcome!"))

    return account  # Retourne immédiatement
```

#### Semaphore - Limiter la concurrence

```python
async def fetch_with_limit(urls: list[str], max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str):
        async with semaphore:  # Max 5 requêtes simultanées
            return await http_client.get(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

---

### 5. FastAPI et Asyncio

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# Endpoint SYNC - bloque le worker
@app.get("/sync")
def sync_endpoint():
    time.sleep(1)  # ⚠️ Bloque tout le worker!
    return {"status": "done"}

# Endpoint ASYNC - libère le worker pendant l'I/O
@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(1)  # ✅ Worker peut servir d'autres requêtes
    return {"status": "done"}

# Background task - fire and forget
@app.post("/users")
async def create_user(data: dict, background_tasks: BackgroundTasks):
    user = await save_user(data)

    # S'exécute après la réponse
    background_tasks.add_task(send_welcome_email, user.email)

    return user
```

#### Quand utiliser async vs sync dans FastAPI ?

| Opération | Sync ou Async |
|-----------|---------------|
| Requête HTTP externe | `async` (httpx) |
| Query DB async | `async` (SQLAlchemy async) |
| Query DB sync | `def` (FastAPI gère) |
| Calcul CPU intensif | `def` + multiprocessing |
| Lecture fichier | `async` (aiofiles) ou `def` |

---

### 6. WebSockets avec FastAPI

```python
from fastapi import FastAPI, WebSocket
from typing import list

app = FastAPI()

# Liste des connexions actives
active_connections: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Attend un message du client
            data = await websocket.receive_text()

            # Broadcast à tous les clients
            for connection in active_connections:
                await connection.send_text(f"Message: {data}")
    except:
        active_connections.remove(websocket)
```

---

## Exercices

### Exercice 1 : Comparer Sync vs Async

Implémente une fonction qui récupère 10 URLs :
1. Version sync (séquentielle)
2. Version async (concurrente)

Compare les temps d'exécution.

→ Fichier : `src/module_02_asyncio/exercice_01_comparison/`

### Exercice 2 : Limiter la concurrence

Implémente un "rate limiter" qui :
- Limite le nombre de requêtes simultanées
- Attend entre les requêtes si nécessaire

→ Fichier : `src/module_02_asyncio/exercice_02_rate_limiter/`

### Exercice 3 : Background Tasks FastAPI

Implémente un endpoint qui :
1. Crée une ressource en DB
2. Envoie une notification en arrière-plan
3. Retourne immédiatement

→ Fichier : `src/module_02_asyncio/exercice_03_background/`

### Exercice 4 : Mini-chat WebSocket

Crée un serveur de chat simple avec :
- Connexion/déconnexion des clients
- Broadcast des messages
- Liste des utilisateurs connectés

→ Fichier : `src/module_02_asyncio/exercice_04_websocket/`

---

## Checkpoint

Avant de passer au module suivant, assure-toi de pouvoir répondre à :

1. **Event loop** : Pourquoi `await asyncio.sleep(1)` est différent de `time.sleep(1)` ?
2. **Tasks** : Quelle est la différence entre `await coro()` et `asyncio.create_task(coro())` ?
3. **FastAPI** : Quand utiliser `def` vs `async def` pour un endpoint ?
4. **Concurrence** : Comment limiter le nombre de requêtes simultanées ?
