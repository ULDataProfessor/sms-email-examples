import os
import requests

MIDJOURNEY_API_URL = os.getenv("MIDJOURNEY_API_URL")
MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY")


def generate_flyer(title: str, date: str, venue: str) -> bytes:
    """Generate an event flyer image using a MidJourney-compatible API."""
    prompt = f"Event flyer for {title} on {date} at {venue}."
    payload = {"prompt": prompt, "api_key": MIDJOURNEY_API_KEY}
    resp = requests.post(MIDJOURNEY_API_URL, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.content
