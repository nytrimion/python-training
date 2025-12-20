# Formation Python - Vue d'ensemble

## Objectif

Transition de développeur senior PHP vers Python, en capitalisant sur l'expertise existante (DDD, Clean Architecture, SOLID) tout en maîtrisant les spécificités Python.

---

## Structure de la Formation

### Module 1 : Fondations Python
**Thèmes** : GIL, long-running processes, syntaxe idiomatique

| Objectif | Statut |
|----------|--------|
| Comprendre le GIL et ses implications | ✅ |
| Maîtriser la différence long-running vs process-per-request | ✅ |
| Écrire du code Python idiomatique (PEP8, type hints) | ✅ |
| Utiliser decorators et context managers | ✅ |
| Maîtriser comprehensions et generators | ✅ |

→ [Accéder au module](./modules/module_01_fondations/README.md)

---

### Module 2 : Asyncio
**Thèmes** : Event loop, async/await, FastAPI async, WebSockets

| Objectif | Statut |
|----------|--------|
| Comprendre l'event loop asyncio | ✅ |
| Maîtriser async/await et les Tasks | ✅ |
| Utiliser asyncio.gather() et create_task() | ✅ |
| Implémenter des endpoints FastAPI async | ✅ |
| Créer un WebSocket simple | ✅ |

→ [Accéder au module](./modules/module_02_asyncio/README.md)

---

### Module 3 : Écosystème Production
**Thèmes** : Celery, SQLAlchemy, pytest

| Objectif | Statut |
|----------|--------|
| Écrire des tests avec pytest | ✅ |
| Utiliser fixtures et mocking | ✅ |
| Modéliser avec SQLAlchemy ORM | ✅ |
| Gérer les migrations avec Alembic | ⬜ |
| Configurer Celery avec Redis | ⬜ |
| Implémenter des tasks avec retry | ⬜ |

→ [Accéder au module](./modules/module_03_ecosysteme/README.md)

---

### Module 4 : Projet Intégrateur
**Thèmes** : EventDispatcher DDD avec 3 implémentations

| Objectif | Statut |
|----------|--------|
| Implémenter SyncEventDispatcher | ⬜ |
| Implémenter AsyncioEventDispatcher | ⬜ |
| Implémenter CeleryEventDispatcher | ⬜ |
| Écrire les tests pour chaque implémentation | ⬜ |
| Créer des benchmarks comparatifs | ⬜ |
| Documenter les trade-offs | ⬜ |

→ [Accéder au module](./modules/module_04_integration/README.md)

---

## Progression Globale

```
Module 1 : Fondations     [✅✅✅✅✅] 100% ✓
Module 2 : Asyncio        [✅✅✅✅✅] 100% ✓
Module 3 : Écosystème     [✅✅✅⬜⬜] 50%
Module 4 : Intégration    [⬜⬜⬜⬜⬜] 0%
─────────────────────────────────────
Total                     [✅✅✅⬜⬜] 62%
```

---

## Ressources

### Documentation
- [Guide d'installation](./01_setup.md)
- [Comparaison PHP/Python](./references/php_python_comparison.md)

### Liens externes
- [Real Python](https://realpython.com/) - Tutorials excellents
- [Python Official Docs](https://docs.python.org/3/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Livres recommandés
- "Fluent Python" - Luciano Ramalho
- "Python Concurrency with asyncio" - Matthew Fowler

---

## Comment utiliser cette formation

1. **Lire** la documentation du module dans `docs/modules/`
2. **Discuter** avec Claude pour clarifier les concepts
3. **Coder** les exercices dans `src/module_XX/`
4. **Tester** avec `pytest tests/module_XX/`
5. **Review** avec Claude pour améliorer le code
6. **Valider** en cochant les objectifs ci-dessus
