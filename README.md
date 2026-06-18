# Space Explorer - SASIKUMAR Sahkana & GUERIN Nam Luân - APP-ING2-LSI1

## Architecture

```
┌──────────────────────────────────────────────────┐
│              CONTROLLER (FastAPI)                │
│        GET /apod  │  GET /asteroids/today        │
├──────────────────────────────────────────────────┤
│  APODService         │  AsteroidService          │
│  → NASA APOD API     │  → NASA NeoWs API         │
├──────────────────────────────────────────────────┤
│         DATA LAYER (Modèles Pydantic)            │
│  APODResponse │ Asteroid │ AsteroidListResponse  │
└──────────────────────────────────────────────────┘
               ↕ Docker Compose ↕
┌──────────────────────────────────────────────────┐
│  Container 1: API (port 8000)                    │
│  Container 2: Frontend Nginx (port 3000)         │
└──────────────────────────────────────────────────┘
```

---

## 2. Lancer l'API en local (sans Docker)

Dans le terminal IntelliJ :
```bash
uvicorn app.main:app --reload
```

Accéder à :
- **API** : http://localhost:8000
- **Swagger** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## 3. Lancer avec Docker Compose

```bash
docker compose up --build
```

- **API** → http://localhost:8000/docs
- **Frontend** → http://localhost:3000

Pour arrêter :
```bash
docker compose down
```

---

## 4. Lancer les tests

### Tous les tests avec couverture
```bash
pytest tests/ --cov=app --cov-report=term-missing -v
```

### Tests par couche uniquement
```bash
# Data layer
pytest tests/test_data/ -v

# Services layer
pytest tests/test_services/ -v

# Controller layer
pytest tests/test_controllers/ -v
```

### Rapport HTML de couverture
```bash
pytest tests/ --cov=app --cov-report=html
# Ouvrir htmlcov/index.html dans le navigateur
```

---

## 5. Qualité du code (Ruff)

```bash
# Vérifier le code
ruff check app/ tests/

# Corriger automatiquement
ruff check app/ tests/ --fix
```

---

## 6. Configurer IntelliJ pour les tests

1. `Run → Edit Configurations → + → pytest`
2. **Script path** : `tests/`
3. **Additional arguments** : `--cov=app -v`
4. **Working directory** : racine du projet
5. Cliquer **OK** → lancer avec le bouton vert

---

## 7. Endpoints de l'API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Health check |
| GET | `/api/v1/apod` | Photo du jour NASA |
| GET | `/api/v1/apod?date=2024-01-15` | Photo d'une date précise |
| GET | `/api/v1/asteroids/today` | Astéroïdes d'aujourd'hui |
| GET | `/api/v1/asteroids/date/2024-01-15` | Astéroïdes d'une date |
| GET | `/api/v1/asteroids/{id}` | Détail d'un astéroïde |

---

## 8. Structure du projet

```
space-explorer/
├── app/
│   ├── data/
│   │   └── models.py          # Modèles Pydantic
│   ├── services/
│   │   ├── apod_service.py    # Service APOD (NASA)
│   │   └── asteroid_service.py # Service Astéroïdes (NASA)
│   ├── controllers/
│   │   └── space_router.py    # Routes FastAPI
│   └── main.py                # Point d'entrée
├── tests/
│   ├── mock_data.py           # Données mock partagées
│   ├── test_data/
│   │   └── test_models.py     # Tests modèles Pydantic
│   ├── test_services/
│   │   ├── test_apod_service.py
│   │   └── test_asteroid_service.py
│   └── test_controllers/
│       └── test_space_router.py
├── frontend/
│   └── index.html             # Frontend (bonus)
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## APIs utilisées

| API | URL | Clé requise                           |
|-----|-----|---------------------------------------|
| NASA APOD | https://api.nasa.gov/planetary/apod   |
| NASA NeoWs| https://api.nasa.gov/neo/rest/v1/feed |