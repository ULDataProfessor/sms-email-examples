"""Print-on-demand production integration."""
import os
import requests
from .config import logger
from .utils import ProductionError

PRINTFUL_URL = os.getenv('PRINTFUL_URL')
PRINTFUL_TOKEN = os.getenv('PRINTFUL_TOKEN')


def create_order(customer: dict, tshirt: dict, design_url: str) -> tuple[str, str]:
    """Send order to print-on-demand service.

    Returns (production_id, estimated_ship_date).
    """
    try:
        payload = {
            'recipient': customer,
            'items': [{
                'variant': f"{tshirt['size']}-{tshirt['color']}",
                'files': [{'url': design_url}],
            }],
        }
        headers = {'Authorization': f'Bearer {PRINTFUL_TOKEN}'}
        resp = requests.post(PRINTFUL_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return str(data.get('id')), data.get('estimated_ship_date')
    except Exception as exc:
        logger.exception("Production order failed")
        raise ProductionError("Production order failed") from exc
