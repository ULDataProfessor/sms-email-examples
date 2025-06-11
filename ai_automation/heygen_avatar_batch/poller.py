"""Utility for polling HeyGen avatar generation status."""

from __future__ import annotations

import time
from typing import Callable, Dict, Any

import requests


class Poller:
    """Poll a status endpoint until generation is complete."""

    def __init__(self, interval: int = 5, timeout: int = 300) -> None:
        self.interval = interval
        self.timeout = timeout

    def poll(self, func: Callable[[], requests.Response]) -> Dict[str, Any]:
        """Polls ``func`` until it returns a completed status or times out."""
        start = time.time()
        while True:
            resp = func()
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "completed":
                return data
            if time.time() - start > self.timeout:
                raise TimeoutError("Avatar generation timed out")
            time.sleep(self.interval)
