"""Client for the VIN decoder service."""

from __future__ import annotations

import requests
import time
from typing import Dict

from ..config import VIN_API_KEY, VIN_API_URL
from ..utils import ExternalAPIError, logger


class VINClient:
    def __init__(self) -> None:
        self.base_url = VIN_API_URL.rstrip("/")
        self.session = requests.Session()
        if VIN_API_KEY:
            self.session.headers.update({"Authorization": f"Bearer {VIN_API_KEY}"})

    def decode(self, vin: str) -> Dict[str, str | int | float]:
        url = f"{self.base_url}/decode/{vin}"
        start = time.perf_counter()
        try:
            resp = self.session.get(url, timeout=5)
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("VIN API error: %s", exc)
            raise ExternalAPIError("VIN decoder failed") from exc
        latency = time.perf_counter() - start
        logger.info("VIN API latency %.3fs", latency)
        return resp.json()
