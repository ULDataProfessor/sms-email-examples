"""Client for generating onboarding videos using the HeyGen avatar API."""

from __future__ import annotations

import os
import requests
from typing import Any

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
HEYGEN_URL = os.getenv("HEYGEN_URL", "https://api.heygen.com/v1")


class VideoClient:
    def __init__(self) -> None:
        if not HEYGEN_API_KEY:
            raise EnvironmentError("HEYGEN_API_KEY must be set")
        self.base_url = HEYGEN_URL.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {HEYGEN_API_KEY}"})

    def generate_video(self, script: str, template_id: str) -> bytes:
        """Request video generation and return binary MP4 data."""
        resp = self.session.post(
            f"{self.base_url}/videos",
            json={"script": script, "template_id": template_id},
        )
        resp.raise_for_status()
        video_url = resp.json().get("video_url")
        if not video_url:
            raise RuntimeError("No video URL returned")
        video_resp = self.session.get(video_url)
        video_resp.raise_for_status()
        return video_resp.content

