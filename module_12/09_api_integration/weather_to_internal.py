"""Fetch weather data and post to an internal service."""
from __future__ import annotations

import os
import requests

WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
TARGET_ENDPOINT = "https://internal.example.com/ingest"


def fetch_weather(city: str, api_key: str) -> dict[str, float | str]:
    resp = requests.get(WEATHER_API, params={"q": city, "appid": api_key, "units": "metric"}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }


def post_weather(payload: dict[str, float | str], url: str = TARGET_ENDPOINT) -> None:
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()


def main() -> None:
    city = os.getenv("CITY", "London")
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    data = fetch_weather(city, api_key)
    post_weather(data)


if __name__ == "__main__":
    main()
