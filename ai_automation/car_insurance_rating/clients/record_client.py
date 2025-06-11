"""Client for the driving record verification service."""

from __future__ import annotations

import requests
import time
from typing import Dict

from ..config import RECORD_API_KEY, RECORD_API_URL
from ..utils import ExternalAPIError, logger


class RecordClient:
    def __init__(self) -> None:
        self.base_url = RECORD_API_URL.rstrip("/")
        self.session = requests.Session()
        if RECORD_API_KEY:
            self.session.headers.update({"Authorization": f"Bearer {RECORD_API_KEY}"})

    def check_history(self, license_years: int, claims: int) -> Dict[str, int]:
        url = f"{self.base_url}/history"
        payload = {"license_years": license_years, "claims": claims}
        start = time.perf_counter()
        try:
            resp = self.session.post(url, json=payload, timeout=5)
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Record API error: %s", exc)
            raise ExternalAPIError("Driving record lookup failed") from exc
        latency = time.perf_counter() - start
        logger.info("Record API latency %.3fs", latency)
        return resp.json()
