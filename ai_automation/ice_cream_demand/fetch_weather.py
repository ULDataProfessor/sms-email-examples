"""Fetch daily weather data from a public API."""

from __future__ import annotations

import requests
import pandas as pd

# Example mapping of location name to latitude and longitude.
# Extend this dictionary with the locations in your sales CSV.
LOCATION_COORDS = {
    "new_york": (40.7128, -74.0060),
    "los_angeles": (34.0522, -118.2437),
}


def fetch_weather(start_date: str, end_date: str, location: str) -> pd.DataFrame:
    """Return daily temperature and precipitation for the date range.

    Parameters
    ----------
    start_date: str
        First date in ``YYYY-MM-DD`` format.
    end_date: str
        Last date in ``YYYY-MM-DD`` format.
    location: str
        Key in ``LOCATION_COORDS`` specifying the city.
    """
    if location not in LOCATION_COORDS:
        raise ValueError(f"Unknown location: {location}")

    lat, lon = LOCATION_COORDS[location]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "UTC",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()["daily"]
    df = pd.DataFrame({
        "date": data["time"],
        "temperature": data["temperature_2m_max"],
        "precipitation": data["precipitation_sum"],
    })
    df["date"] = pd.to_datetime(df["date"])
    df["location"] = location
    return df
