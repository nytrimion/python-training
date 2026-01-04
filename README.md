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
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (pour PostgreSQL et Redis)

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
| **2. Asyncio**     | Event loop, async/await, FastAPI, WebSockets     | ✅      |
| **3. Écosystème**  | Celery, SQLAlchemy, pytest                       | ✅      |
| **4. Intégration** | Projet EventDispatcher DDD                       | ✅      |

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

## Docker

Les modules 3 et 4 nécessitent PostgreSQL et Redis. Ces services sont fournis via Docker Compose.

### Services disponibles

| Service    | Container           | Port  | URL de connexion                                         |
|------------|---------------------|-------|----------------------------------------------------------|
| PostgreSQL | `training_postgres` | 5432  | `postgresql://training:training@localhost:5432/training` |
| Redis      | `training_redis`    | 6379  | `redis://localhost:6379/0`                               |

### Commandes Docker

```bash
# Démarrer les services en arrière-plan
docker-compose up -d

# Voir l'état des services
docker-compose ps

# Voir les logs (suivre en temps réel)
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f postgres

# Arrêter les services (conserve les données)
docker-compose stop

# Arrêter et supprimer les conteneurs
docker-compose down

# Tout supprimer (conteneurs + volumes/données)
docker-compose down -v

# Redémarrer un service
docker-compose restart postgres

# Accéder au shell PostgreSQL
docker exec -it training_postgres psql -U training

# Accéder au CLI Redis
docker exec -it training_redis redis-cli
```

## Documentation

- [Vue d'ensemble et progression](docs/00_overview.md)
- [Guide d'installation](docs/01_setup.md)
- [Comparaison PHP/Python](docs/references/php_python_comparison.md)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.