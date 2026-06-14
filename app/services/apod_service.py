import httpx
from app.data.models import APODResponse

NASA_BASE_URL = "https://api.nasa.gov"


class APODService:
    """Service for NASA Astronomy Picture of the Day API."""

    def __init__(self, api_key: str = "KrVBixAMRPibikKOBY0OdymP7O2AQh2IfwKDFBZh", client: httpx.AsyncClient = None):
        self.api_key = api_key
        self._client = client  # permet l'injection pour les tests

    async def _get_client(self):
        if self._client:
            return self._client
        return httpx.AsyncClient()

    async def get_apod(self, date: str = None) -> APODResponse:
        """
        Récupère la photo astronomique du jour (ou d'une date donnée).
        :param date: format YYYY-MM-DD (optionnel)
        :raises httpx.HTTPStatusError: si la NASA renvoie une erreur
        :raises ValueError: si la réponse est inattendue
        """
        params = {"api_key": self.api_key}
        if date:
            params["date"] = date

        client = await self._get_client()
        try:
            response = await client.get(f"{NASA_BASE_URL}/planetary/apod", params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_apod(data)
        finally:
            if not self._client:
                await client.aclose()

    def _parse_apod(self, data: dict) -> APODResponse:
        return APODResponse(
            title=data["title"],
            date=data["date"],
            explanation=data["explanation"],
            url=data["url"],
            media_type=data.get("media_type", "image"),
            copyright=data.get("copyright"),
        )
