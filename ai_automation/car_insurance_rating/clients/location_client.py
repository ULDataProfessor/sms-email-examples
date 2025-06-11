"""Client for the location risk service."""

from __future__ import annotations

import requests
import time
from typing import Dict

from ..config import LOCATION_API_KEY, LOCATION_API_URL
from ..utils import ExternalAPIError, logger


class LocationClient:
    def __init__(self) -> None:
        self.base_url = LOCATION_API_URL.rstrip("/")
        self.session = requests.Session()
        if LOCATION_API_KEY:
            self.session.headers.update({"Authorization": f"Bearer {LOCATION_API_KEY}"})

    def risk_for_postal(self, postal_code: str) -> Dict[str, float]:
        url = f"{self.base_url}/risk/{postal_code}"
        start = time.perf_counter()
        try:
            resp = self.session.get(url, timeout=5)
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Location API error: %s", exc)
            raise ExternalAPIError("Location risk lookup failed") from exc
        latency = time.perf_counter() - start
        logger.info("Location API latency %.3fs", latency)
        return resp.json()
