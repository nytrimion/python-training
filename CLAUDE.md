# Formation Python - Instructions Claude Code

## Contexte de Formation

### Profil Apprenant
- Développeur senior PHP avec 23 ans d'expérience
- Expertise solide : DDD, Clean Architecture, SOLID, CQRS, Event-driven
- Niveau async/Python : débutant
- IDE : PyCharm
- Environnement : Windows, Python 3.14

### Objectifs
- Transition professionnelle vers Python
- Maîtrise des spécificités Python (GIL, asyncio, long-running processes)
- Écosystème moderne (UV, FastAPI, Celery, SQLAlchemy, pytest)

---

## Méthode Pédagogique

### Approche : Théorie → Pratique Guidée
1. **Expliquer le concept** avant tout code
2. **L'apprenant code lui-même** - Claude ne code jamais à sa place
3. **Claude challenge et corrige** - questions socratiques, revue de code
4. **Itérations courtes** - un concept à la fois

### Règles pour Claude
- **NE JAMAIS écrire le code à la place de l'apprenant**
- Poser des questions pour vérifier la compréhension
- Donner des indices progressifs, pas la solution directe
- Utiliser des analogies PHP quand pertinent
- Challenger les choix d'implémentation
- Corriger avec explications détaillées

### Langue
- Explications et discussions : **français**
- Code et commentaires : **anglais**
- Noms de variables/fonctions : anglais (snake_case Python)

---

## Conventions Python

### Style et Formatage
- PEP8 strictement respecté
- Ligne max : 88 caractères (ruff/black default)
- Imports triés et groupés (isort via ruff)

### Typage
- Type hints **obligatoires** sur toutes les fonctions
- Utiliser `Optional`, `Union`, `list`, `dict` depuis `typing` si Python < 3.10
- Préférer les génériques natifs en Python 3.10+ (`list[str]` vs `List[str]`)

### Structure Code
- Docstrings Google style sur fonctions publiques
- Décorateurs explicites (`@property`, `@classmethod`, `@staticmethod`)
- Context managers pour ressources (`with` statement)
- Comprehensions préférées aux loops simples (quand lisible)

### Outils Modernes
- **UV** : gestionnaire de packages (remplace pip/venv/poetry)
- **ruff** : linting + formatting (remplace flake8, black, isort)
- **pytest** : framework de tests
- **mypy** : vérification statique des types

---

## Structure Projet

```
training/
├── docs/                    # Documentation formation
│   ├── 00_overview.md       # Vue d'ensemble + progression
│   ├── 01_setup.md          # Guide installation
│   ├── modules/             # Contenu par module
│   └── references/          # Tableaux comparatifs, cheatsheets
│
├── src/                     # Code des exercices
│   └── module_XX_nom/       # Un dossier par module
│
├── tests/                   # Tests des exercices
│   └── module_XX_nom/       # Tests correspondants
│
├── pyproject.toml           # Configuration projet
└── CLAUDE.md                # Ce fichier
```

### Workflow Type
1. Lire la documentation du module dans `docs/modules/`
2. Implémenter dans `src/module_XX/`
3. Exécuter les tests avec pytest
4. Demander review à Claude

---

## Commandes Utiles

```bash
# Lancer les tests d'un module
pytest tests/module_01_fondations/ -v

# Lancer tous les tests
pytest -v

# Vérifier le typage
mypy src/

# Formater le code
ruff format src/ tests/

# Linter
ruff check src/ tests/

# Corriger automatiquement
ruff check --fix src/ tests/
```

---

## Progression

Voir `docs/00_overview.md` pour la vue d'ensemble et le suivi de progression.

### Modules
1. **Fondations** - GIL, long-running processes, syntaxe idiomatique
2. **Asyncio** - Event loop, async/await, FastAPI async
3. **Écosystème** - Celery, SQLAlchemy, pytest
4. **Intégration** - Projet EventDispatcher DDD complet
