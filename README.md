# Formation Python

Formation Python pour développeur senior PHP - Transition vers l'écosystème Python moderne.

## Objectif

Maîtriser les spécificités Python en capitalisant sur l'expertise existante (DDD, Clean Architecture, SOLID).

## Prérequis

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) (gestionnaire de packages moderne)

## Installation rapide

```bash
# 1. Installer UV (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Synchroniser les dépendances
uv sync

# 3. Vérifier l'installation
uv run python --version
```

## Structure du projet

```
training/
├── CLAUDE.md                 # Instructions Claude Code
├── pyproject.toml            # Configuration projet
│
├── docs/                     # Documentation
│   ├── 00_overview.md        # Vue d'ensemble + progression
│   ├── 01_setup.md           # Guide d'installation détaillé
│   ├── modules/              # Contenu par module
│   │   ├── module_01_fondations/   # GIL, long-running, syntaxe
│   │   ├── module_02_asyncio/      # Event loop, async/await
│   │   ├── module_03_ecosysteme/   # Celery, SQLAlchemy, pytest
│   │   └── module_04_integration/  # Projet DDD complet
│   └── references/           # Comparaisons PHP/Python
│
├── src/                      # Code des exercices
└── tests/                    # Tests
```

## Modules

| Module | Thèmes |
|--------|--------|
| **1. Fondations** | GIL, long-running processes, syntaxe idiomatique |
| **2. Asyncio** | Event loop, async/await, FastAPI, WebSockets |
| **3. Écosystème** | Celery, SQLAlchemy, pytest |
| **4. Intégration** | Projet EventDispatcher DDD |

## Commandes utiles

```bash
# Lancer les tests
uv run pytest

# Linter le code
uv run ruff check src/ tests/

# Formater le code
uv run ruff format src/ tests/

# Vérifier les types
uv run mypy src/
```

## Documentation

- [Vue d'ensemble](docs/00_overview.md)
- [Guide d'installation](docs/01_setup.md)
- [Comparaison PHP/Python](docs/references/php_python_comparison.md)