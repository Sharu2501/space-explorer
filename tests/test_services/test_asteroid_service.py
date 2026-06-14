"""Tests unitaires du service Asteroid avec mock HTTP (respx)."""
import pytest
import httpx
import respx
from app.services.asteroid_service import AsteroidService
from app.data.models import Asteroid, AsteroidListResponse
from tests.mock_data import MOCK_ASTEROID_FEED, MOCK_SINGLE_ASTEROID


@pytest.fixture
def asteroid_service():
    return AsteroidService(api_key="TEST_KEY")


class TestAsteroidService:

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_asteroids_for_date(self, asteroid_service):
        """Test récupération des astéroïdes pour une date."""
        respx.get("https://api.nasa.gov/neo/rest/v1/feed").mock(
            return_value=httpx.Response(200, json=MOCK_ASTEROID_FEED)
        )
        result = await asteroid_service.get_asteroids_for_date("2024-01-15")

        assert isinstance(result, AsteroidListResponse)
        assert result.count == 2
        assert result.date == "2024-01-15"
        assert len(result.asteroids) == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_today_asteroids(self, asteroid_service):
        """Test récupération des astéroïdes d'aujourd'hui."""
        respx.get("https://api.nasa.gov/neo/rest/v1/feed").mock(
            return_value=httpx.Response(200, json=MOCK_ASTEROID_FEED)
        )
        result = await asteroid_service.get_today_asteroids()

        assert isinstance(result, AsteroidListResponse)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_asteroid_by_id(self, asteroid_service):
        """Test récupération d'un astéroïde par ID."""
        respx.get("https://api.nasa.gov/neo/rest/v1/neo/3542519").mock(
            return_value=httpx.Response(200, json=MOCK_SINGLE_ASTEROID)
        )
        result = await asteroid_service.get_asteroid_by_id("3542519")

        assert isinstance(result, Asteroid)
        assert result.id == "3542519"
        assert result.name == "(2010 PK9)"
        assert result.is_potentially_hazardous is False

    @respx.mock
    @pytest.mark.asyncio
    async def test_asteroid_hazardous_flag(self, asteroid_service):
        """Test qu'un astéroïde dangereux est bien identifié."""
        respx.get("https://api.nasa.gov/neo/rest/v1/feed").mock(
            return_value=httpx.Response(200, json=MOCK_ASTEROID_FEED)
        )
        result = await asteroid_service.get_asteroids_for_date("2024-01-15")

        hazardous = [a for a in result.asteroids if a.is_potentially_hazardous]
        assert len(hazardous) == 1
        assert hazardous[0].name == "(2099 DANGER)"

    @respx.mock
    @pytest.mark.asyncio
    async def test_asteroid_not_found(self, asteroid_service):
        """Test gestion d'un ID inexistant."""
        respx.get("https://api.nasa.gov/neo/rest/v1/neo/000").mock(
            return_value=httpx.Response(404, json={"error": "Not found"})
        )
        with pytest.raises(Exception):
            await asteroid_service.get_asteroid_by_id("000")

    def test_parse_asteroid_with_close_approach(self, asteroid_service):
        """Test parsing complet d'un astéroïde avec close approach."""
        result = asteroid_service._parse_single_asteroid(MOCK_SINGLE_ASTEROID)

        assert result.close_approach is not None
        assert result.close_approach.date == "2024-01-15"
        assert result.close_approach.velocity.km_per_second == 12.5
        assert result.close_approach.miss_distance.lunar == 11.7

    def test_parse_asteroid_without_close_approach(self, asteroid_service):
        """Test parsing d'un astéroïde sans close approach."""
        data = {**MOCK_SINGLE_ASTEROID, "close_approach_data": []}
        result = asteroid_service._parse_single_asteroid(data)

        assert result.close_approach is None

    def test_parse_asteroid_list_empty(self, asteroid_service):
        """Test parsing d'une liste vide."""
        data = {"near_earth_objects": {"2024-01-15": []}}
        result = asteroid_service._parse_asteroid_list(data, "2024-01-15")

        assert result.count == 0
        assert result.asteroids == []
