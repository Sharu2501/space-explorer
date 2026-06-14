from fastapi import APIRouter, HTTPException, Query
from app.services.apod_service import APODService
from app.services.asteroid_service import AsteroidService
from app.data.models import APODResponse, AsteroidListResponse, Asteroid
import os

router = APIRouter()

NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    raise RuntimeError("NASA_API_KEY n'est pas définie")

apod_service = APODService(api_key=NASA_API_KEY)
asteroid_service = AsteroidService(api_key=NASA_API_KEY)


# ─── APOD ────────────────────────────────────────────────────────────────────

# ─── APOD ────────────────────────────────────────────────────────────────────

@router.get("/apod", response_model=APODResponse, summary="Photo astronomique du jour")
async def get_apod(date: str = Query(None, description="Date au format YYYY-MM-DD")):
    """
    Retourne la photo astronomique du jour NASA (APOD).
    Paramètre optionnel : date (YYYY-MM-DD).
    """
    # Si le front-end envoie une chaîne vide "" ou des espaces, on repasse à None
    if date and not date.strip():
        date = None

    try:
        return await apod_service.get_apod(date=date)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur NASA APOD : {str(e)}")

# ─── Asteroids ───────────────────────────────────────────────────────────────

@router.get("/asteroids/today", response_model=AsteroidListResponse, summary="Astéroïdes du jour")
async def get_today_asteroids():
    """Retourne les astéroïdes proches de la Terre aujourd'hui."""
    try:
        return await asteroid_service.get_today_asteroids()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur NASA NeoWs : {str(e)}")


@router.get("/asteroids/date/{target_date}", response_model=AsteroidListResponse, summary="Astéroïdes par date")
async def get_asteroids_by_date(target_date: str):
    """
    Retourne les astéroïdes pour une date donnée.
    Format : YYYY-MM-DD
    """
    try:
        return await asteroid_service.get_asteroids_for_date(target_date)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur NASA NeoWs : {str(e)}")


@router.get("/asteroids/{asteroid_id}", response_model=Asteroid, summary="Détail d'un astéroïde")
async def get_asteroid_detail(asteroid_id: str):
    """Retourne les détails d'un astéroïde par son ID NASA."""
    try:
        return await asteroid_service.get_asteroid_by_id(asteroid_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur NASA NeoWs : {str(e)}")
