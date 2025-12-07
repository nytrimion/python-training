# Guide d'Installation

Ce guide te permettra de configurer un environnement Python moderne avec UV, ruff, pytest et mypy.

---

## 1. Installation de UV

UV est le nouveau gestionnaire de packages Python, développé par Astral (créateurs de ruff). Il remplace pip, venv et poetry avec des performances 10-100x supérieures.

### Windows (PowerShell)

```powershell
# Installation de UV
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Vérifier l'installation
uv --version
```

### Pourquoi UV ?

| Aspect | pip/venv | UV |
|--------|----------|-----|
| Installation deps | ~30s | ~1s |
| Lock file | ❌ Non | ✅ Oui |
| Résolution deps | Basique | Avancée |
| Écrit en | Python | Rust |

---

## 2. Initialisation du Projet

```powershell
# Se placer dans le dossier du projet
cd C:\Users\ouryd\PycharmProjects\training

# Supprimer l'ancien venv (optionnel, UV va le recréer)
Remove-Item -Recurse -Force .venv

# Initialiser avec UV (crée pyproject.toml si absent)
uv init

# Synchroniser les dépendances
uv sync
```

---

## 3. Installation des Dépendances

### Dépendances principales

```powershell
# Framework web
uv add fastapi uvicorn[standard]

# ORM et base de données
uv add sqlalchemy alembic

# Task queue
uv add celery redis

# HTTP client
uv add httpx

# Validation
uv add pydantic
```

### Dépendances de développement

```powershell
# Testing
uv add --dev pytest pytest-asyncio pytest-cov

# Linting et formatting
uv add --dev ruff

# Type checking
uv add --dev mypy
```

---

## 4. Configuration PyCharm

### Configurer l'interpréteur Python

1. **File → Settings → Project → Python Interpreter**
2. Cliquer sur l'engrenage → **Add Interpreter**
3. Sélectionner **Existing** → naviguer vers `.venv\Scripts\python.exe`
4. Appliquer

### Configurer ruff comme formateur

1. **File → Settings → Tools → External Tools**
2. Ajouter un nouvel outil :
   - Name: `Ruff Format`
   - Program: `$ProjectFileDir$\.venv\Scripts\ruff.exe`
   - Arguments: `format $FilePath$`
   - Working directory: `$ProjectFileDir$`

### Raccourci clavier pour formatter

1. **File → Settings → Keymap**
2. Chercher "Ruff Format"
3. Assigner un raccourci (ex: `Ctrl+Alt+L`)

---

## 5. Commandes Utiles

### Gestion des dépendances (UV)

```powershell
# Ajouter une dépendance
uv add <package>

# Ajouter une dépendance dev
uv add --dev <package>

# Mettre à jour les dépendances
uv sync

# Voir les dépendances installées
uv pip list
```

### Linting et Formatting (ruff)

```powershell
# Vérifier le code
uv run ruff check src/ tests/

# Corriger automatiquement
uv run ruff check --fix src/ tests/

# Formater le code
uv run ruff format src/ tests/
```

### Tests (pytest)

```powershell
# Lancer tous les tests
uv run pytest

# Tests d'un module spécifique
uv run pytest tests/module_01_fondations/ -v

# Avec coverage
uv run pytest --cov=src --cov-report=term-missing
```

### Type checking (mypy)

```powershell
# Vérifier les types
uv run mypy src/
```

---

## 6. Vérification de l'Installation

Crée un fichier `test_setup.py` à la racine :

```python
"""Test de vérification de l'environnement."""
import sys


def main() -> None:
    """Vérifie que l'environnement est correctement configuré."""
    print(f"Python version: {sys.version}")

    # Test des imports
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI non installé")

    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy non installé")

    try:
        import pytest
        print(f"✅ pytest {pytest.__version__}")
    except ImportError:
        print("❌ pytest non installé")

    try:
        import ruff
        print("✅ ruff installé")
    except ImportError:
        print("❌ ruff non installé")

    print("\n🎉 Setup terminé !")


if __name__ == "__main__":
    main()
```

Exécute-le :

```powershell
uv run python test_setup.py
```

---

## 7. Structure Finale du Projet

Après le setup, ton projet devrait ressembler à ceci :

```
training/
├── .venv/                  # Environnement virtuel (géré par UV)
├── pyproject.toml          # Configuration projet
├── uv.lock                 # Lock file des dépendances
├── CLAUDE.md               # Instructions Claude Code
├── docs/                   # Documentation
├── src/                    # Code des exercices
└── tests/                  # Tests
```

---

## Problèmes Courants

### UV non reconnu après installation

Ferme et rouvre PowerShell, ou ajoute UV au PATH :

```powershell
$env:Path += ";$env:USERPROFILE\.local\bin"
```

### Conflit avec l'ancien venv

Supprime l'ancien venv et laisse UV le recréer :

```powershell
Remove-Item -Recurse -Force .venv
uv sync
```

### PyCharm ne trouve pas les packages

Reconfigure l'interpréteur Python en pointant vers `.venv\Scripts\python.exe`.
