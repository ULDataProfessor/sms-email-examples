"""Shipping and tracking integration."""
import os
import time
import requests
from .config import logger
from .utils import ShippingError

SHIPPING_URL_TEMPLATE = os.getenv('SHIPPING_URL_TEMPLATE')


def wait_for_tracking(production_id: str, attempts: int = 10, delay: int = 30) -> str:
    """Poll shipping API until a tracking URL is available."""
    try:
        for _ in range(attempts):
            url = SHIPPING_URL_TEMPLATE.format(production_id=production_id)
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            tracking = data.get('tracking_url')
            if tracking:
                return tracking
            time.sleep(delay)
        raise ShippingError('Tracking not available')
    except Exception as exc:
        logger.exception('Shipping tracking failed')
        raise ShippingError('Shipping tracking failed') from exc
