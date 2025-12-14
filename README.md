# 🐍 Formation Python - De PHP Senior à Python Expert

> Formation pratique assistée par Claude Code pour développeurs PHP expérimentés

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Learning%20Mode-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## À propos

Cette formation a été conçue pour les **développeurs seniors PHP** souhaitant maîtriser Python en capitalisant sur leur
expertise existante (DDD, Clean Architecture, SOLID, CQRS).

**Approche pédagogique :**

- 🎯 Théorie → Pratique guidée
- 🤖 Assistée par Claude Code (mode Learning)
- 📝 L'apprenant code lui-même, Claude guide et corrige
- 🔄 Analogies PHP/Python pour faciliter la transition

## Comment utiliser cette formation

1. **Cloner le repo** et installer les dépendances avec UV
2. **Ouvrir avec Claude Code** (`claude` dans le terminal)
3. **Suivre les modules** dans l'ordre ([docs/00_overview.md](docs/00_overview.md))
4. **Coder les exercices** — Claude ne code pas à ta place !

## Prérequis

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) (gestionnaire de packages moderne)

## Installation rapide

```bash
# 1. Cloner le repo
git clone https://github.com/nytrimion/training-python.git
cd training-python

# 2. Installer UV (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Synchroniser les dépendances
uv sync

# 4. Vérifier l'installation
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

| Module             | Thèmes                                           | Statut |
|--------------------|--------------------------------------------------|--------|
| **1. Fondations**  | GIL, long-running processes, syntaxe idiomatique | ✅      |
| **2. Asyncio**     | Event loop, async/await, FastAPI, WebSockets     | ⬜      |
| **3. Écosystème**  | Celery, SQLAlchemy, pytest                       | ⬜      |
| **4. Intégration** | Projet EventDispatcher DDD                       | ⬜      |

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

- [Vue d'ensemble et progression](docs/00_overview.md)
- [Guide d'installation](docs/01_setup.md)
- [Comparaison PHP/Python](docs/references/php_python_comparison.md)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.