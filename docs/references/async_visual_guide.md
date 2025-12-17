# Python Async - Guide Visuel

## Vue d'ensemble : Les 3 modèles de concurrence

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           PROCESSUS PYTHON                                │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                              GIL                                    │  │
│  │         (Global Interpreter Lock - 1 seul thread exécute            │  │
│  │                    du bytecode Python à la fois)                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                                 │
│  │ Thread 1 │  │ Thread 2 │  │ Thread 3 │   ← Partagent le GIL            │
│  │  (main)  │  │          │  │          │                                 │
│  └──────────┘  └──────────┘  └──────────┘                                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ PROCESSUS PYTHON 2  │  │ PROCESSUS PYTHON 3  │  │ PROCESSUS PYTHON 4  │
│   (multiprocessing) │  │   (multiprocessing) │  │   (multiprocessing) │
│  ┌───────────────┐  │  │  ┌───────────────┐  │  │  ┌───────────────┐  │
│  │   GIL séparé  │  │  │  │   GIL séparé  │  │  │  │   GIL séparé  │  │
│  └───────────────┘  │  │  └───────────────┘  │  │  └───────────────┘  │
│  ┌──────────┐       │  │  ┌──────────┐       │  │  ┌──────────┐       │
│  │ Thread 1 │       │  │  │ Thread 1 │       │  │  │ Thread 1 │       │
│  └──────────┘       │  │  └──────────┘       │  │  └──────────┘       │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
        ↑                        ↑                        ↑
        └────────────────────────┴────────────────────────┘
                    Vrais parallélisme CPU
                    (contourne le GIL)
```

---

## Comparaison des 3 approches

```
┌────────────────┬─────────────────┬─────────────────┬─────────────────────┐
│                │   THREADING     │ MULTIPROCESSING │      ASYNCIO        │
├────────────────┼─────────────────┼─────────────────┼─────────────────────┤
│ Unité          │ Thread          │ Process         │ Coroutine (Task)    │
│ Mémoire        │ Partagée        │ Séparée (IPC)   │ Partagée            │
│ GIL            │ Bloqué (CPU)    │ Contourné       │ Non concerné        │
│ Overhead       │ Moyen           │ Élevé           │ Très faible         │
│ Cas d'usage    │ I/O legacy      │ CPU-bound       │ I/O moderne         │
│ Complexité     │ Race conditions │ IPC complexe    │ Simple (await)      │
└────────────────┴─────────────────┴─────────────────┴─────────────────────┘
```

---

## Le GIL en action

### Travail CPU-bound (calculs)

```
THREADING avec CPU-bound : PAS de parallélisme réel
═══════════════════════════════════════════════════

Thread 1: ████████░░░░░░░░████████░░░░░░░░████████
Thread 2: ░░░░░░░░████████░░░░░░░░████████░░░░░░░░
          ↑       ↑       ↑       ↑       ↑
          GIL     GIL     GIL     GIL     GIL
          T1      T2      T1      T2      T1

Temps total: ~2x (pas d'amélioration, overhead en plus!)


MULTIPROCESSING avec CPU-bound : VRAI parallélisme
══════════════════════════════════════════════════

Process 1: ████████████████████████████████
Process 2: ████████████████████████████████
           └──────────────────────────────┘
                   Exécution simultanée

Temps total: ~1x (divisé par nombre de cores)
```

### Travail I/O-bound (réseau, fichiers, DB)

```
THREADING avec I/O-bound : Parallélisme effectif
════════════════════════════════════════════════

Thread 1: ██──────────────██     (██ = CPU, ── = I/O wait)
Thread 2: ░░██──────────────██░░
Thread 3: ░░░░██──────────────██
              ↑
         GIL libéré pendant I/O !

Temps total: ~1x (les I/O se chevauchent)


ASYNCIO avec I/O-bound : Même résultat, 1 seul thread
═════════════════════════════════════════════════════

Event Loop (1 thread):
  t=0ms   Coroutine 1: start fetch ──┐
  t=0ms   Coroutine 2: start fetch ──┼── Toutes démarrent
  t=0ms   Coroutine 3: start fetch ──┘   immédiatement

          ... le thread attend les I/O ...

  t=100ms Coroutine 2: done ←── première réponse
  t=120ms Coroutine 1: done
  t=150ms Coroutine 3: done

Temps total: ~max(latences) au lieu de sum(latences)
```

---

## ASYNCIO en détail

### L'Event Loop - Chef d'orchestre

```
┌─────────────────────────────────────────────────────────────────┐
│                         EVENT LOOP                              │
│                      (1 seul thread)                            │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    FILE D'ATTENTE                       │   │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │   │
│   │  │ Task 1 │ │ Task 2 │ │ Task 3 │ │ Task 4 │  ...       │   │
│   │  │ READY  │ │WAITING │ │ READY  │ │WAITING │            │   │
│   │  └────────┘ └────────┘ └────────┘ └────────┘            │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                     EXÉCUTION                           │   │
│   │                                                         │   │
│   │  1. Prend une tâche READY                               │   │
│   │  2. Exécute jusqu'au prochain 'await'                   │   │
│   │  3. Si await I/O → marque WAITING, passe à la suivante  │   │
│   │  4. Quand I/O terminé → marque READY                    │   │
│   │  5. Répète                                              │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### await - Point de suspension

```python
async def fetch_user(user_id: int) -> User:
    print("Début")  # ← Exécuté immédiatement

    await db.query(...)  # ← SUSPENSION: "Je libère l'event loop"
    #   L'event loop peut exécuter d'autres tâches
    #   Quand la DB répond → reprend ici

    print("Fin")  # ← Exécuté après la réponse DB
    return user
```

```
TIMELINE - Une seule coroutine
══════════════════════════════

fetch_user(1):  ██████──────────────────────██████
                  ↑                            ↑
               print                        print
               "Début"                      "Fin"
                      └── await db.query ──┘
                          (thread libre)
```

---

## Patterns ASYNCIO comparés

### 1. await séquentiel

```python
result1 = await fetch(url1)  # Attend 1s
result2 = await fetch(url2)  # Attend 1s
result3 = await fetch(url3)  # Attend 1s
# Total: 3s
```

```
TIMELINE
════════
fetch(url1): ████████████████████
fetch(url2):                     ████████████████████
fetch(url3):                                          ████████████████████
             |___________________|___________________|____________________|
             0s                  1s                  2s                   3s
```

### 2. asyncio.gather() - Concurrence

```python
results = await asyncio.gather(
    fetch(url1),
    fetch(url2),
    fetch(url3),
)
# Total: ~1s (max des 3)
```

```
TIMELINE
════════
fetch(url1): ████████████████████
fetch(url2): ████████████████████
fetch(url3): ████████████████████
             |___________________|
             0s                  1s

Les 3 coroutines démarrent en même temps !
```

### 3. asyncio.create_task() - Fire and forget

```python
task = asyncio.create_task(send_email())  # Démarre immédiatement
# ... continue sans attendre ...
result = await task  # Optionnel: récupérer le résultat plus tard
```

```
TIMELINE
════════
main():       ████░░░░░░░░░░░░████████████
                 ↑              ↑
           create_task     await task
                 │              │
send_email():    ████████████████
                 └── s'exécute en parallèle ──┘
```

### 4. Semaphore - Concurrence limitée

```python
semaphore = asyncio.Semaphore(2)  # Max 2 simultanées


async def limited_fetch(url):
    async with semaphore:
        return await fetch(url)
```

```
TIMELINE (5 URLs, max 2 concurrentes)
═════════════════════════════════════
Slot 1: ████████████████████          ████████████████████
Slot 2: ████████████████████████████████████████████████████████
        url1              url3        url5
                url2              url4
        |___________________|_________|___________________|
        0s                  1s        1.5s                2.5s
```

---

## create_task() vs BackgroundTasks (FastAPI)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        asyncio.create_task()                            │
├─────────────────────────────────────────────────────────────────────────┤
│ • Démarre IMMÉDIATEMENT dans l'event loop                               │
│ • La tâche s'exécute pendant que ton code continue                      │
│ • Tu peux await le résultat plus tard                                   │
│ • Usage: concurrence dans une même fonction                             │
│                                                                         │
│   async def handler():                                                  │
│       task = asyncio.create_task(slow_operation())  ← démarre ici       │
│       do_something_else()                           ← pendant que ça    │
│       result = await task                           ← récupère après    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     FastAPI BackgroundTasks                             │
├─────────────────────────────────────────────────────────────────────────┤
│ • S'exécute APRÈS l'envoi de la réponse HTTP                            │
│ • Le client n'attend pas                                                │
│ • Pas de moyen de récupérer le résultat                                 │
│ • Usage: fire-and-forget (emails, logs, analytics)                      │
│                                                                         │
│   async def handler(background_tasks: BackgroundTasks):                 │
│       result = await save_to_db()                                       │
│       background_tasks.add_task(send_email)  ← planifié, pas exécuté    │
│       return result                          ← réponse envoyée          │
│       # send_email() s'exécute maintenant                               │
└─────────────────────────────────────────────────────────────────────────┘
```

```
TIMELINE COMPARÉE
═════════════════

create_task():
  Request: ════════════════════════════════════════►
  Handler: ████████████████████████████████████████
  Task:         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                ↑                              ↑
           create_task                    await task
  Response:                                        ════►


BackgroundTasks:
  Request: ════════════════════►
  Handler: ████████████████████
  Response:                    ════► (client reçoit ici)
  BgTask:                           ░░░░░░░░░░░░░░░░░░░░░░░░
                                    ↑
                              démarre APRÈS la réponse
```

---

## FastAPI : def vs async def

```
┌───────────────────────────────────────────────────────────────────────┐
│                           FastAPI SERVER                              │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        EVENT LOOP                               │  │
│  │                     (thread principal)                          │  │
│  │                                                                 │  │
│  │   async def endpoint():     ← S'exécute directement ici         │  │
│  │       await db.query()      ← Libère l'event loop               │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                              │                                        │
│                              ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                      THREAD POOL                                │  │
│  │                  (threads secondaires)                          │  │
│  │                                                                 │  │
│  │   def endpoint():           ← Exécuté dans un thread séparé     │  │
│  │       db.query()            ← Bloque CE thread, pas l'event loop│  │
│  │                                                                 │  │
│  │   Thread 1: [endpoint_sync_1]                                   │  │
│  │   Thread 2: [endpoint_sync_2]                                   │  │
│  │   Thread 3: [libre]                                             │  │
│  │   ...                                                           │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

### Règle de choix

```
┌──────────────────────────────────────┬──────────────────────────────────┐
│           async def                  │              def                 │
├──────────────────────────────────────┼──────────────────────────────────┤
│ • Client HTTP async (httpx)          │ • ORM sync (SQLAlchemy sync)     │
│ • DB async (asyncpg, SQLAlchemy 2.0) │ • Librairie sync legacy          │
│ • Cache async (aioredis)             │ • Calculs CPU (⚠️ éviter)        │
│ • Fichiers (aiofiles)                │ • Fichiers (standard open())     │
├──────────────────────────────────────┴──────────────────────────────────┤
│                                                                         │
│  ⚠️ PIÈGE COURANT:                                                      │
│                                                                         │
│  async def bad_endpoint():                                              │
│      time.sleep(1)      # ❌ BLOQUE tout l'event loop !                 │
│      requests.get(url)  # ❌ BLOQUE tout l'event loop !                 │
│                                                                         │
│  Si tu utilises async def, TOUT doit être async dedans.                 │
│  Sinon utilise def (FastAPI gère via thread pool).                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## WebSockets - Connexions persistantes

### HTTP vs WebSocket

```
HTTP (Request/Response) - "Envoyer des lettres"
═══════════════════════════════════════════════

Client                              Server
  │                                    │
  │─── GET /messages ─────────────────>│  Requête
  │<── [message1, message2] ───────────│  Réponse
  │                                    │
  │    (connexion fermée)              │
  │                                    │
  │─── GET /messages ─────────────────>│  Nouvelle requête (polling)
  │<── [message1, message2, message3]──│  Réponse
  │                                    │

  ⚠️ Le serveur ne peut PAS envoyer sans requête du client
  ⚠️ Overhead : nouvelle connexion TCP à chaque requête


WebSocket (Bidirectionnel) - "Ligne téléphonique"
═════════════════════════════════════════════════

Client                              Server
  │                                    │
  │─── HTTP Upgrade: websocket ───────>│  Handshake
  │<── 101 Switching Protocols ────────│
  │                                    │
  │====== CONNEXION PERSISTANTE =======│
  │                                    │
  │─── "Hello" ───────────────────────>│  Client envoie
  │<── "Hi there!" ────────────────────│  Server répond
  │                                    │
  │<── "New notification!" ────────────│  Server PUSH (sans requête!)
  │<── "Another update!" ──────────────│  Server PUSH
  │                                    │
  │─── "Bye" ─────────────────────────>│  Client envoie
  │<── "Goodbye!" ─────────────────────│  Server répond
  │                                    │
  │══════ Connexion fermée ════════════│

  ✅ Bidirectionnel : les deux peuvent envoyer à tout moment
  ✅ Pas de polling : le serveur push quand il veut
  ✅ Faible latence : connexion déjà établie
```

### Architecture WebSocket avec FastAPI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FastAPI SERVER                                    │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          EVENT LOOP                                   │  │
│  │                                                                       │  │
│  │   ┌──────────────────────────────────────────────────────────────┐    │  │
│  │   │              GESTIONNAIRE DE CONNEXIONS                      │    │  │
│  │   │                                                              │    │  │
│  │   │   active_connections: list[WebSocket]                        │    │  │
│  │   │                                                              │    │  │
│  │   │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │  │
│  │   │   │ Client 1 │ │ Client 2 │ │ Client 3 │ │ Client 4 │ ...    │    │  │
│  │   │   │    WS    │ │    WS    │ │    WS    │ │    WS    │        │    │  │
│  │   │   └──────────┘ └──────────┘ └──────────┘ └──────────┘        │    │  │
│  │   │                                                              │    │  │
│  │   └──────────────────────────────────────────────────────────────┘    │  │
│  │                                                                       │  │
│  │   Pour chaque connexion WebSocket :                                   │  │
│  │   ┌──────────────────────────────────────────────────────────────┐    │  │
│  │   │ async def websocket_endpoint(websocket: WebSocket):          │    │  │
│  │   │     await websocket.accept()        # Handshake              │    │  │
│  │   │     while True:                     # Boucle infinie         │    │  │
│  │   │         data = await websocket.receive_text()  # ATTEND      │    │  │
│  │   │         # ↑ Non-bloquant! L'event loop gère d'autres clients │    │  │
│  │   │         await websocket.send_text(f"Echo: {data}")           │    │  │
│  │   └──────────────────────────────────────────────────────────────┘    │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Timeline - Chat avec 3 clients

```
TIMELINE - Mini chat WebSocket
══════════════════════════════

Event Loop (1 thread gère TOUT) :

Client 1: ═══════════════════════════════════════════════════════════════════
          │connect│─────await receive─────│"Hi"│──────await receive──────│...
                                             │
Client 2: ══════════════════════════════════════════════════════════════════
               │connect│─────await receive──────────│"Hello"│──await recv──
                                                        │
Client 3: ══════════════════════════════════════════════════════════════════
                    │connect│─────────await receive───────────────│"Hey"│──

Broadcast: Quand Client 1 dit "Hi":
           ├─→ send_text("User1: Hi") à Client 2
           └─→ send_text("User1: Hi") à Client 3

Les 3 connexions sont gérées en CONCURRENCE par 1 seul thread !
Chaque "await receive" libère l'event loop pour les autres.
```

---

## Résumé mental

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     COMMENT CHOISIR ?                                     ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Travail CPU intensif ?                                                  ║
║        │                                                                  ║
║        ├─ OUI → multiprocessing (contourne le GIL)                        ║
║        │                                                                  ║
║        └─ NON → Travail I/O ?                                             ║
║                    │                                                      ║
║                    ├─ OUI, librairie async → asyncio (await)              ║
║                    │                                                      ║
║                    ├─ OUI, librairie sync  → threading ou def (FastAPI)   ║
║                    │                                                      ║
║                    └─ NON → code synchrone normal                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════╗
║                     BLOQUANT vs NON-BLOQUANT                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   BLOQUANT (le thread dort, ne fait RIEN) :                               ║
║   • time.sleep()                                                          ║
║   • requests.get()                                                        ║
║   • open().read()                                                         ║
║   • cursor.execute() (psycopg2 sync)                                      ║
║                                                                           ║
║   NON-BLOQUANT (le thread peut faire autre chose) :                       ║
║   • await asyncio.sleep()                                                 ║
║   • await httpx.get()                                                     ║
║   • await aiofiles.open()                                                 ║
║   • await connection.execute() (asyncpg)                                  ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Patterns WebSocket courants

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│      PATTERN         │                    USAGE                            │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Echo                 │ Renvoie le message reçu (test, debug)               │
│ Broadcast            │ Envoie à TOUS les clients (chat, notifications)     │
│ Room/Channel         │ Envoie aux clients d'un groupe (chat rooms, games)  │
│ Pub/Sub              │ Clients s'abonnent à des topics (real-time feeds)   │
│ Request/Response     │ Client demande, server répond (RPC over WS)         │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

### Gestion des déconnexions

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Process message...

    except WebSocketDisconnect:
        # Client s'est déconnecté (ferme l'onglet, perte réseau, etc.)
        connections.remove(websocket)

    finally:
        # Nettoyage garanti
        if websocket in connections:
            connections.remove(websocket)
```

```
TIMELINE - Déconnexion
══════════════════════

Client:  ══════════════════════════╳ (ferme l'onglet)
                                   │
Server:  ──await receive───────────┤
                                   │
         WebSocketDisconnect raised!
                                   │
         → except block s'exécute
         → remove(websocket)
         → Coroutine se termine proprement
```

---

## Analogies finales

| Python Async    | Monde réel                                           |
|-----------------|------------------------------------------------------|
| Event Loop      | Chef de cuisine qui distribue les tâches             |
| Coroutine       | Une recette en cours de préparation                  |
| `await`         | "Le plat est au four, je peux faire autre chose"     |
| `create_task()` | "Lance cette recette en parallèle"                   |
| `gather()`      | "Prépare ces 3 plats en même temps"                  |
| `Semaphore`     | "Max 2 fours disponibles"                            |
| Thread          | Un cuisinier                                         |
| Process         | Une cuisine entière (avec son propre chef)           |
| GIL             | "Un seul cuisinier peut utiliser le plan de travail" |
| WebSocket       | Ligne téléphonique ouverte (vs HTTP = envoyer des lettres) |