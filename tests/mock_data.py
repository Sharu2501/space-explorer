"""Données mock réutilisables dans tous les tests."""

MOCK_APOD_RESPONSE = {
    "title": "The Pillars of Creation",
    "date": "2024-01-15",
    "explanation": "Dark pillars of gas and dust extend from the Eagle Nebula.",
    "url": "https://apod.nasa.gov/apod/image/2401/pillars.jpg",
    "media_type": "image",
    "copyright": "NASA/ESA/Hubble",
}

MOCK_ASTEROID_FEED = {
    "near_earth_objects": {
        "2024-01-15": [
            {
                "id": "3542519",
                "name": "(2010 PK9)",
                "is_potentially_hazardous_asteroid": False,
                "estimated_diameter": {
                    "kilometers": {
                        "estimated_diameter_min": 0.123,
                        "estimated_diameter_max": 0.275,
                    }
                },
                "close_approach_data": [
                    {
                        "close_approach_date": "2024-01-15",
                        "relative_velocity": {
                            "kilometers_per_second": "12.5",
                            "kilometers_per_hour": "45000.0",
                        },
                        "miss_distance": {
                            "kilometers": "4500000.0",
                            "lunar": "11.7",
                        },
                    }
                ],
                "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=3542519",
            },
            {
                "id": "9999999",
                "name": "(2099 DANGER)",
                "is_potentially_hazardous_asteroid": True,
                "estimated_diameter": {
                    "kilometers": {
                        "estimated_diameter_min": 0.8,
                        "estimated_diameter_max": 1.2,
                    }
                },
                "close_approach_data": [],
                "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=9999999",
            },
        ]
    }
}

MOCK_SINGLE_ASTEROID = {
    "id": "3542519",
    "name": "(2010 PK9)",
    "is_potentially_hazardous_asteroid": False,
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 0.123,
            "estimated_diameter_max": 0.275,
        }
    },
    "close_approach_data": [
        {
            "close_approach_date": "2024-01-15",
            "relative_velocity": {
                "kilometers_per_second": "12.5",
                "kilometers_per_hour": "45000.0",
            },
            "miss_distance": {
                "kilometers": "4500000.0",
                "lunar": "11.7",
            },
        }
    ],
    "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=3542519",
}
