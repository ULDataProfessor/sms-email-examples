"""Generate AI postcard art from uploaded photos."""

import base64
import os
import time
from pathlib import Path
from typing import Tuple

import requests

from .config import logger
from .utils import DesignError

MIDJOURNEY_URL = os.getenv("MIDJOURNEY_URL")
MIDJOURNEY_TOKEN = os.getenv("MIDJOURNEY_TOKEN")


def generate_art(photo_path: Path, style_prompt: str) -> Tuple[str, bytes]:
    """Submit photo to the AI art service and return the image URL and content."""
    try:
        logger.debug("Encoding photo %s", photo_path)
        data_b64 = base64.b64encode(photo_path.read_bytes()).decode()
        payload = {"prompt": style_prompt, "image": data_b64, "token": MIDJOURNEY_TOKEN}
        logger.info("Submitting art generation request")
        resp = requests.post(MIDJOURNEY_URL, json=payload, timeout=15)
        resp.raise_for_status()
        job = resp.json()["job_id"]

        logger.debug("Polling job %s", job)
        for _ in range(30):
            poll = requests.get(f"{MIDJOURNEY_URL}/{job}", timeout=10)
            poll.raise_for_status()
            data = poll.json()
            if data.get("status") == "done":
                image_url = data["image_url"]
                image_resp = requests.get(image_url, timeout=10)
                image_resp.raise_for_status()
                return image_url, image_resp.content
            time.sleep(2)
        raise DesignError("Timeout waiting for art generation")
    except Exception as exc:  # broad exception for demo
        logger.error("Design generation failed: %s", exc)
        raise DesignError(str(exc)) from exc
