"""Design generation module."""
import os
import requests
from .config import logger
from .utils import DesignError

MIDJOURNEY_API_URL = os.getenv('MIDJOURNEY_API_URL')
S3_BUCKET_URL = os.getenv('S3_BUCKET_URL')


def generate_design(prompt: str) -> str:
    """Generate design image and upload to cloud storage.

    Returns public URL of uploaded image.
    """
    try:
        response = requests.post(MIDJOURNEY_API_URL, json={"prompt": prompt}, timeout=30)
        response.raise_for_status()
        image_data = response.content
        # Upload to storage (placeholder)
        upload_resp = requests.post(S3_BUCKET_URL, files={"file": image_data}, timeout=30)
        upload_resp.raise_for_status()
        url = upload_resp.json().get("url")
        if not url:
            raise DesignError("Upload failed")
        return url
    except Exception as exc:
        logger.exception("Design generation failed")
        raise DesignError("Design generation failed") from exc
