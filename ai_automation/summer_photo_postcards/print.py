"""Interact with the print-on-demand API."""

import os
from datetime import datetime, timedelta
from typing import Dict

import requests

from .config import logger
from .utils import PrintError

PRINT_API_URL = os.getenv("PRINT_API_URL")
PRINT_API_KEY = os.getenv("PRINT_API_KEY")


def create_postcard_order(image_url: str, quantity: int, customer: Dict[str, str]) -> Dict[str, str]:
    """Submit the postcard print job and return order info."""
    try:
        payload = {
            "image_url": image_url,
            "quantity": quantity,
            "customer": customer,
            "api_key": PRINT_API_KEY,
        }
        logger.info("Creating print order")
        resp = requests.post(PRINT_API_URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("order_id"):
            raise PrintError("Invalid response from print API")
        # Fake ship date if not provided
        ship_date = data.get("ship_date") or (datetime.utcnow() + timedelta(days=3)).isoformat()
        return {"order_id": data["order_id"], "ship_date": ship_date}
    except Exception as exc:  # for demo purposes
        logger.error("Print order failed: %s", exc)
        raise PrintError(str(exc)) from exc
