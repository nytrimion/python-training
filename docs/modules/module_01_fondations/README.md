# Module 1 : Fondations Python

## Objectifs d'apprentissage

À la fin de ce module, tu seras capable de :
- [ ] Expliquer le GIL et ses implications sur la concurrence
- [ ] Comprendre la différence entre process-per-request (PHP) et long-running (Python)
- [ ] Écrire du code Python idiomatique respectant PEP8
- [ ] Utiliser les type hints de manière systématique
- [ ] Maîtriser les decorators et context managers
- [ ] Utiliser les comprehensions et generators efficacement

---

## Contenu

### 1. Le GIL (Global Interpreter Lock)

#### Concept clé
Le GIL est un verrou qui empêche plusieurs threads Python d'exécuter du bytecode simultanément. C'est une spécificité de CPython (l'implémentation standard).

#### Ce que tu dois comprendre
- Le GIL limite le **threading CPU-bound**, pas I/O-bound
- Pour le calcul intensif → utilise `multiprocessing`
- Pour l'I/O concurrent → `asyncio` (le GIL n'est pas un problème)

#### Analogie PHP
```
PHP-FPM      = multiprocessing natif (1 process = 1 requête)
Python + GIL = 1 process peut servir N requêtes, mais 1 thread CPU à la fois
```

#### Ressources
- [Understanding the Python GIL](https://realpython.com/python-gil/)
- [Python docs - Threading](https://docs.python.org/3/library/threading.html)

---

### 2. Long-running Processes vs Process-per-Request

#### Concept clé
En PHP traditionnel, chaque requête HTTP démarre un nouveau process.
En Python (FastAPI/Django), un process reste actif et sert N requêtes.

#### Implications majeures

| Aspect | PHP | Python |
|--------|-----|--------|
| Bootstrap | Chaque requête (10-50ms) | Une fois au démarrage |
| Connexions DB | Reconnexion à chaque fois | Connection pool persistant |
| Cache | Nécessite Redis | Simple `dict` en mémoire |
| État partagé | Impossible | Possible (avec précaution) |

#### Ce que tu dois retenir
- **Avantage** : performance (pas de re-bootstrap)
- **Piège** : memory leaks, état partagé non voulu
- **Bonne pratique** : restart périodique des workers

---

### 3. Syntaxe et Idiomes Python

#### PEP8 - Conventions de nommage

```python
# Variables et fonctions : snake_case
user_name = "John"
def get_user_by_id(user_id: int) -> User:
    pass

# Classes : PascalCase
class UserRepository:
    pass

# Constantes : UPPER_SNAKE_CASE
MAX_RETRIES = 3
DATABASE_URL = "postgresql://..."

# Privé : préfixe underscore
_internal_cache = {}
def _helper_function():
    pass
```

#### Type hints

```python
from typing import Optional

# Fonction avec types
def greet(name: str, times: int = 1) -> str:
    return f"Hello {name}! " * times

# Optional pour nullable
def find_user(user_id: int) -> Optional[User]:
    return db.get(user_id)  # Peut retourner None

# Collections (Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

---

### 4. Decorators

#### Concept
Un decorator est une fonction qui "enveloppe" une autre fonction pour modifier son comportement.

```python
import functools
import time

def timer(func):
    """Mesure le temps d'exécution d'une fonction."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "done"
```

#### Decorators courants
- `@property` - Getter comme attribut
- `@staticmethod` - Méthode sans `self`
- `@classmethod` - Méthode avec `cls`
- `@functools.lru_cache` - Cache automatique

---

### 5. Context Managers

#### Concept
Le `with` statement garantit le nettoyage des ressources, même en cas d'exception.

```python
# Fichier - fermeture automatique
with open("file.txt", "r") as f:
    content = f.read()
# f est automatiquement fermé ici

# Connexion DB
with db.connect() as conn:
    conn.execute("SELECT * FROM users")
# conn est automatiquement fermée

# Lock threading
from threading import Lock

lock = Lock()
with lock:
    # Section critique
    shared_resource.update()
# Lock libéré automatiquement
```

---

### 6. Comprehensions et Generators

#### List comprehension

```python
# ❌ PHP-style
numbers = []
for i in range(10):
    if i % 2 == 0:
        numbers.append(i ** 2)

# ✅ Pythonic
numbers = [i ** 2 for i in range(10) if i % 2 == 0]
```

#### Dict comprehension

```python
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Créer un dict indexé par id
users_by_id = {u["id"]: u for u in users}
```

#### Generators (lazy evaluation)

```python
# ❌ Charge tout en mémoire
def get_all_lines(file_path):
    with open(file_path) as f:
        return f.readlines()  # Liste complète

# ✅ Lazy - une ligne à la fois
def get_all_lines(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()

# Utilisation
for line in get_all_lines("huge_file.txt"):
    process(line)  # Une ligne à la fois en mémoire
```

---

## Exercices

### Exercice 1 : Observer le GIL

Implémente un script qui compare les performances de :
1. Threading sur une tâche CPU-bound (calcul)
2. Threading sur une tâche I/O-bound (requêtes HTTP simulées)
3. Multiprocessing sur une tâche CPU-bound

→ Fichier : `src/module_01_fondations/exercice_01_gil/`

### Exercice 2 : Réécrire une classe PHP

Prends une classe PHP simple et réécris-la en Python idiomatique avec :
- Type hints complets
- Properties au lieu de getters/setters
- Context manager si applicable

→ Fichier : `src/module_01_fondations/exercice_02_class/`

### Exercice 3 : Créer un decorator

Implémente un decorator `@retry(max_attempts=3)` qui :
- Réessaye une fonction en cas d'exception
- Attend un délai exponentiel entre les tentatives
- Log chaque tentative

→ Fichier : `src/module_01_fondations/exercice_03_decorator/`

---

## Checkpoint

Avant de passer au module suivant, assure-toi de pouvoir répondre à :

1. **GIL** : Pourquoi asyncio n'est pas limité par le GIL ?
2. **Long-running** : Quel piège éviter avec les variables globales ?
3. **Idiomes** : Quelle est la différence entre `@property` et `@staticmethod` ?
4. **Generators** : Quand préférer un generator à une list comprehension ?
