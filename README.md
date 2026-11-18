# Senior Task Service

Brique fonctionnelle isolée démontrant une **architecture senior** contre le code jetable des « vibe coders ».

## Technologies

- **Backend** : Python 3.10+, FastAPI, Pydantic v2, Pytest
- **Frontend** : TypeScript, React, Tailwind CSS (composant isolé)

## Architecture

```
backend/
├── app/
│   ├── schemas.py      # Modèles Pydantic étanches (validation frontière)
│   ├── repository.py   # Port + adapter in-memory (prêt pour PostgreSQL)
│   ├── service.py      # Logique métier pure, testable
│   └── main.py         # Couche HTTP fine
└── tests/
    └── test_service.py # Couverture des chemins critiques – 100% passed
```

### Principes appliqués

- Typage strict (Pydantic + Enums + UUID)
- Séparation des couches (API / Service / Repository)
- Validation métier (date passée, titre vide, règle « pas de réouverture de tâche DONE »)
- Tests unitaires systématiques avant tout commit
- Modèles de données étanches (`extra="forbid"`, validators)

## Installation & Tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
# → tous les tests doivent passer (100%)
```

Lancer l’API :

```bash
uvicorn app.main:app --reload
```

## Frontend

Le composant `TaskList.tsx` est prêt à être intégré dans une app React + Tailwind.  
Il consomme le contrat `TaskResponse` de l’API.

## Pull Request

Voir le message de commit et la description détaillée dans l’historique Git.

**Objectif atteint** : code maintenable, testé, typé, documenté.
