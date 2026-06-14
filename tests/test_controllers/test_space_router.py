"""Tests de la couche Controller (routes FastAPI) avec mock des services."""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.data.models import APODResponse, AsteroidListResponse, Asteroid, AsteroidDiameter, AsteroidCloseApproach, AsteroidVelocity, AsteroidMissDistance

client = TestClient(app)


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_apod():
    return APODResponse(
        title="The Pillars of Creation",
        date="2024-01-15",
        explanation="A great nebula.",
        url="https://apod.nasa.gov/apod/image/2401/pillars.jpg",
        media_type="image",
        copyright="NASA",
    )


@pytest.fixture
def mock_asteroid_list():
    return AsteroidListResponse(
        count=1,
        date="2024-01-15",
        asteroids=[
            Asteroid(
                id="3542519",
                name="(2010 PK9)",
                is_potentially_hazardous=False,
                diameter=AsteroidDiameter(min_km=0.123, max_km=0.275),
                close_approach=AsteroidCloseApproach(
                    date="2024-01-15",
                    velocity=AsteroidVelocity(km_per_second=12.5, km_per_hour=45000.0),
                    miss_distance=AsteroidMissDistance(km=4500000.0, lunar=11.7),
                ),
                nasa_url="https://nasa.gov",
            )
        ],
    )


@pytest.fixture
def mock_single_asteroid():
    return Asteroid(
        id="3542519",
        name="(2010 PK9)",
        is_potentially_hazardous=False,
        diameter=AsteroidDiameter(min_km=0.123, max_km=0.275),
        nasa_url="https://nasa.gov",
    )


# ─── Root ─────────────────────────────────────────────────────────────────────

class TestRoot:
    def test_health_check(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# ─── APOD Controller ─────────────────────────────────────────────────────────

class TestAPODController:

    def test_get_apod_success(self, mock_apod):
        with patch("app.controllers.space_router.apod_service") as mock_service:
            mock_service.get_apod = AsyncMock(return_value=mock_apod)

            response = client.get("/api/v1/apod")

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "The Pillars of Creation"
            assert data["media_type"] == "image"

    def test_get_apod_with_date(self, mock_apod):
        with patch("app.controllers.space_router.apod_service") as mock_service:
            mock_service.get_apod = AsyncMock(return_value=mock_apod)

            response = client.get("/api/v1/apod?date=2024-01-15")

            assert response.status_code == 200

    def test_get_apod_service_error(self):
        with patch("app.controllers.space_router.apod_service") as mock_service:
            mock_service.get_apod = AsyncMock(side_effect=Exception("NASA down"))

            response = client.get("/api/v1/apod")

            assert response.status_code == 502
            assert "APOD" in response.json()["detail"]


# ─── Asteroid Controller ──────────────────────────────────────────────────────

class TestAsteroidController:

    def test_get_today_asteroids(self, mock_asteroid_list):
        with patch("app.controllers.space_router.asteroid_service") as mock_service:
            mock_service.get_today_asteroids = AsyncMock(return_value=mock_asteroid_list)

            response = client.get("/api/v1/asteroids/today")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 1
            assert data["asteroids"][0]["name"] == "(2010 PK9)"

    def test_get_asteroids_by_date(self, mock_asteroid_list):
        with patch("app.controllers.space_router.asteroid_service") as mock_service:
            mock_service.get_asteroids_for_date = AsyncMock(return_value=mock_asteroid_list)

            response = client.get("/api/v1/asteroids/date/2024-01-15")

            assert response.status_code == 200
            assert response.json()["date"] == "2024-01-15"

    def test_get_asteroid_by_id(self, mock_single_asteroid):
        with patch("app.controllers.space_router.asteroid_service") as mock_service:
            mock_service.get_asteroid_by_id = AsyncMock(return_value=mock_single_asteroid)

            response = client.get("/api/v1/asteroids/3542519")

            assert response.status_code == 200
            assert response.json()["id"] == "3542519"

    def test_get_today_asteroids_service_error(self):
        with patch("app.controllers.space_router.asteroid_service") as mock_service:
            mock_service.get_today_asteroids = AsyncMock(side_effect=Exception("API timeout"))

            response = client.get("/api/v1/asteroids/today")

            assert response.status_code == 502

    def test_asteroid_response_structure(self, mock_asteroid_list):
        with patch("app.controllers.space_router.asteroid_service") as mock_service:
            mock_service.get_today_asteroids = AsyncMock(return_value=mock_asteroid_list)

            response = client.get("/api/v1/asteroids/today")
            asteroid = response.json()["asteroids"][0]

            # Vérification structure complète
            assert "id" in asteroid
            assert "name" in asteroid
            assert "is_potentially_hazardous" in asteroid
            assert "diameter" in asteroid
            assert "min_km" in asteroid["diameter"]
            assert "max_km" in asteroid["diameter"]
