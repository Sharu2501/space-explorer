"""Tests unitaires du service APOD avec mock HTTP (respx)."""
import pytest
import httpx
import respx
from app.services.apod_service import APODService
from app.data.models import APODResponse
from tests.mock_data import MOCK_APOD_RESPONSE


@pytest.fixture
def apod_service():
    return APODService(api_key="TEST_KEY")


class TestAPODService:

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_apod_success(self, apod_service):
        """Test récupération APOD avec succès."""
        respx.get("https://api.nasa.gov/planetary/apod").mock(
            return_value=httpx.Response(200, json=MOCK_APOD_RESPONSE)
        )
        result = await apod_service.get_apod()

        assert isinstance(result, APODResponse)
        assert result.title == "The Pillars of Creation"
        assert result.date == "2024-01-15"
        assert result.media_type == "image"
        assert result.copyright == "NASA/ESA/Hubble"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_apod_with_date(self, apod_service):
        """Test APOD avec une date spécifique."""
        respx.get("https://api.nasa.gov/planetary/apod").mock(
            return_value=httpx.Response(200, json=MOCK_APOD_RESPONSE)
        )
        result = await apod_service.get_apod(date="2024-01-15")

        assert result.date == "2024-01-15"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_apod_without_copyright(self, apod_service):
        """Test APOD sans copyright (champ optionnel)."""
        data = {**MOCK_APOD_RESPONSE}
        del data["copyright"]

        respx.get("https://api.nasa.gov/planetary/apod").mock(
            return_value=httpx.Response(200, json=data)
        )
        result = await apod_service.get_apod()

        assert result.copyright is None

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_apod_nasa_error(self, apod_service):
        """Test gestion d'une erreur HTTP de la NASA."""
        respx.get("https://api.nasa.gov/planetary/apod").mock(
            return_value=httpx.Response(429, json={"error": "Rate limit exceeded"})
        )
        with pytest.raises(Exception):
            await apod_service.get_apod()

    def test_parse_apod_valid(self, apod_service):
        """Test unitaire du parsing APOD."""
        result = apod_service._parse_apod(MOCK_APOD_RESPONSE)

        assert result.title == "The Pillars of Creation"
        assert result.url == "https://apod.nasa.gov/apod/image/2401/pillars.jpg"

    def test_parse_apod_video(self, apod_service):
        """Test parsing d'une APOD de type vidéo."""
        data = {**MOCK_APOD_RESPONSE, "media_type": "video"}
        result = apod_service._parse_apod(data)

        assert result.media_type == "video"
