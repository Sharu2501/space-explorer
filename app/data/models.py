from pydantic import BaseModel
from typing import Optional


# ─── APOD Models ────────────────────────────────────────────────────────────

class APODResponse(BaseModel):
    title: str
    date: str
    explanation: str
    url: str
    media_type: str
    copyright: Optional[str] = None


# ─── Asteroid Models ─────────────────────────────────────────────────────────

class AsteroidDiameter(BaseModel):
    min_km: float
    max_km: float


class AsteroidVelocity(BaseModel):
    km_per_second: float
    km_per_hour: float


class AsteroidMissDistance(BaseModel):
    km: float
    lunar: float


class AsteroidCloseApproach(BaseModel):
    date: str
    velocity: AsteroidVelocity
    miss_distance: AsteroidMissDistance


class Asteroid(BaseModel):
    id: str
    name: str
    is_potentially_hazardous: bool
    diameter: AsteroidDiameter
    close_approach: Optional[AsteroidCloseApproach] = None
    nasa_url: str


class AsteroidListResponse(BaseModel):
    count: int
    date: str
    asteroids: list[Asteroid]
