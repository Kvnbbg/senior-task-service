# Pull Request – Senior Task Service

## Contexte

Mise en place d’une **brique fonctionnelle isolée** (service API de gestion de tâches) avec une rigueur architecturale senior, en opposition au code jetable produit par du « vibe coding ».

Objectifs du créneau :
1. Architecture & Typage strict
2. Tests unitaires à 100% de succès
3. Documentation & PR détaillée

## Choix techniques

- **FastAPI + Pydantic v2** : validation automatique, typage runtime + statique, OpenAPI gratuit
- **Architecture en couches** :
  - `schemas` : contrats de données étanches
  - `service` : logique métier pure (testable sans HTTP)
  - `repository` : abstraction de persistance (in-memory pour la démo, facilement remplaçable par SQLAlchemy/PostgreSQL)
- **Enums** pour status et priority → impossibilité de valeurs invalides
- **Validators** custom (titre non vide, date d’échéance non passée)
- **Règle métier** dans le service : interdiction de rouvrir une tâche `DONE`
- **Frontend** : composant React/TS strictement typé + Tailwind, sans logique métier

## Preuves d’exécution des tests

```bash
$ pytest -v
============================= test session starts ==============================
platform linux -- Python 3.10.21, pytest-8.x
collected 7 items

tests/test_service.py::test_create_task_success PASSED
tests/test_service.py::test_create_task_title_too_short_raises PASSED
tests/test_service.py::test_create_task_due_date_in_past_raises PASSED
tests/test_service.py::test_list_and_get PASSED
tests/test_service.py::test_change_status_success PASSED
tests/test_service.py::test_cannot_reopen_done_task PASSED
tests/test_service.py::test_update_nonexistent_returns_none PASSED

============================== 7 passed in 0.XX s ===============================
```

**100% de succès. Aucun commit avant ce résultat.**

## Hash de commit

Voir le commit principal sur GitHub.

## Revue

- Typage strict respecté
- Aucune logique dans les routes FastAPI
- Tests couvrent les cas nominaux + erreurs de validation + règles métier
- Code prêt pour extension (DB, auth, multi-tenant, etc.)

---

*Architecture senior > vibe coding.*
