"""Tests unitaires de la couche Data (modèles Pydantic)."""
import pytest
from pydantic import ValidationError

from app.data.models import (
    APODResponse,
    Asteroid,
    AsteroidCloseApproach,
    AsteroidDiameter,
    AsteroidListResponse,
    AsteroidMissDistance,
    AsteroidVelocity,
)


class TestAPODResponse:
    def test_valid_apod(self):
        apod = APODResponse(
            title="Pillars of Creation",
            date="2024-01-15",
            explanation="Dark nebula pillars...",
            url="https://example.com/img.jpg",
            media_type="image",
        )
        assert apod.title == "Pillars of Creation"
        assert apod.copyright is None  # champ optionnel

    def test_apod_with_copyright(self):
        apod = APODResponse(
            title="Test",
            date="2024-01-15",
            explanation="Desc",
            url="https://example.com/img.jpg",
            media_type="image",
            copyright="NASA",
        )
        assert apod.copyright == "NASA"

    def test_apod_missing_required_field(self):
        with pytest.raises(ValidationError):
            APODResponse(title="No URL", date="2024-01-15", explanation="Desc", media_type="image")


class TestAsteroidDiameter:
    def test_valid_diameter(self):
        d = AsteroidDiameter(min_km=0.1, max_km=0.5)
        assert d.min_km == 0.1
        assert d.max_km == 0.5

    def test_diameter_zero(self):
        d = AsteroidDiameter(min_km=0.0, max_km=0.0)
        assert d.min_km == 0.0


class TestAsteroidVelocity:
    def test_valid_velocity(self):
        v = AsteroidVelocity(km_per_second=12.5, km_per_hour=45000.0)
        assert v.km_per_second == 12.5
        assert v.km_per_hour == 45000.0


class TestAsteroidMissDistance:
    def test_valid_miss_distance(self):
        m = AsteroidMissDistance(km=4500000.0, lunar=11.7)
        assert m.km == 4500000.0
        assert m.lunar == 11.7


class TestAsteroidCloseApproach:
    def test_valid_close_approach(self):
        ca = AsteroidCloseApproach(
            date="2024-01-15",
            velocity=AsteroidVelocity(km_per_second=12.5, km_per_hour=45000.0),
            miss_distance=AsteroidMissDistance(km=4500000.0, lunar=11.7),
        )
        assert ca.date == "2024-01-15"
        assert ca.velocity.km_per_second == 12.5
        assert ca.miss_distance.lunar == 11.7


class TestAsteroid:
    def test_valid_asteroid(self):
        a = Asteroid(
            id="3542519",
            name="(2010 PK9)",
            is_potentially_hazardous=False,
            diameter=AsteroidDiameter(min_km=0.1, max_km=0.3),
            nasa_url="https://nasa.gov",
        )
        assert a.id == "3542519"
        assert a.is_potentially_hazardous is False
        assert a.close_approach is None

    def test_hazardous_asteroid(self):
        a = Asteroid(
            id="1",
            name="DANGER",
            is_potentially_hazardous=True,
            diameter=AsteroidDiameter(min_km=1.0, max_km=2.0),
            nasa_url="https://nasa.gov",
        )
        assert a.is_potentially_hazardous is True


class TestAsteroidListResponse:
    def test_empty_list(self):
        r = AsteroidListResponse(count=0, date="2024-01-15", asteroids=[])
        assert r.count == 0
        assert r.asteroids == []

    def test_list_with_items(self):
        asteroids = [
            Asteroid(
                id=str(i),
                name=f"Asteroid {i}",
                is_potentially_hazardous=False,
                diameter=AsteroidDiameter(min_km=0.1, max_km=0.5),
                nasa_url="https://nasa.gov",
            )
            for i in range(3)
        ]
        r = AsteroidListResponse(count=3, date="2024-01-15", asteroids=asteroids)
        assert r.count == 3
        assert len(r.asteroids) == 3
