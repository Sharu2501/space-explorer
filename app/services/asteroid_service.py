import httpx
from datetime import date
from app.data.models import Asteroid, AsteroidListResponse, AsteroidDiameter, AsteroidVelocity, AsteroidMissDistance, AsteroidCloseApproach

NASA_BASE_URL = "https://api.nasa.gov"


class AsteroidService:
    """Service for NASA Near Earth Object Web Service (NeoWs)."""

    def __init__(self, api_key: str = "KrVBixAMRPibikKOBY0OdymP7O2AQh2IfwKDFBZh", client: httpx.AsyncClient = None):
        self.api_key = api_key
        self._client = client

    async def _get_client(self):
        if self._client:
            return self._client
        return httpx.AsyncClient()

    async def get_today_asteroids(self) -> AsteroidListResponse:
        """Récupère les astéroïdes proches de la Terre aujourd'hui."""
        today = date.today().isoformat()
        return await self._get_asteroids_for_date(today)

    async def get_asteroids_for_date(self, target_date: str) -> AsteroidListResponse:
        """Récupère les astéroïdes pour une date donnée (YYYY-MM-DD)."""
        return await self._get_asteroids_for_date(target_date)

    async def _get_asteroids_for_date(self, target_date: str) -> AsteroidListResponse:
        params = {
            "start_date": target_date,
            "end_date": target_date,
            "api_key": self.api_key,
        }

        client = await self._get_client()
        try:
            response = await client.get(f"{NASA_BASE_URL}/neo/rest/v1/feed", params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_asteroid_list(data, target_date)
        finally:
            if not self._client:
                await client.aclose()

    async def get_asteroid_by_id(self, asteroid_id: str) -> Asteroid:
        """Récupère le détail d'un astéroïde par son ID NASA."""
        params = {"api_key": self.api_key}

        client = await self._get_client()
        try:
            response = await client.get(
                f"{NASA_BASE_URL}/neo/rest/v1/neo/{asteroid_id}", params=params
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_single_asteroid(data)
        finally:
            if not self._client:
                await client.aclose()

    def _parse_asteroid_list(self, data: dict, target_date: str) -> AsteroidListResponse:
        raw_list = data.get("near_earth_objects", {}).get(target_date, [])
        asteroids = [self._parse_single_asteroid(a) for a in raw_list]
        return AsteroidListResponse(
            count=len(asteroids),
            date=target_date,
            asteroids=asteroids,
        )

    def _parse_single_asteroid(self, data: dict) -> Asteroid:
        # Diamètre
        diam = data.get("estimated_diameter", {}).get("kilometers", {})
        diameter = AsteroidDiameter(
            min_km=diam.get("estimated_diameter_min", 0.0),
            max_km=diam.get("estimated_diameter_max", 0.0),
        )

        # Close approach (première entrée si disponible)
        close_approach = None
        approaches = data.get("close_approach_data", [])
        if approaches:
            ca = approaches[0]
            vel = ca.get("relative_velocity", {})
            miss = ca.get("miss_distance", {})
            close_approach = AsteroidCloseApproach(
                date=ca.get("close_approach_date", ""),
                velocity=AsteroidVelocity(
                    km_per_second=float(vel.get("kilometers_per_second", 0)),
                    km_per_hour=float(vel.get("kilometers_per_hour", 0)),
                ),
                miss_distance=AsteroidMissDistance(
                    km=float(miss.get("kilometers", 0)),
                    lunar=float(miss.get("lunar", 0)),
                ),
            )

        return Asteroid(
            id=str(data["id"]),
            name=data["name"],
            is_potentially_hazardous=data.get("is_potentially_hazardous_asteroid", False),
            diameter=diameter,
            close_approach=close_approach,
            nasa_url=data.get("nasa_jpl_url", ""),
        )
