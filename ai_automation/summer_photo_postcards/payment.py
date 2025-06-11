"""Charge customers via Stripe."""

import os

import stripe

from .config import logger
from .utils import PaymentError

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
stripe.api_key = STRIPE_API_KEY

UNIT_PRICE = float(os.getenv("UNIT_PRICE", "2.50"))
SHIPPING_COST = float(os.getenv("SHIPPING_COST", "5.00"))
TAX_RATE = float(os.getenv("TAX_RATE", "0.05"))


def charge_customer(token: str, quantity: int) -> str:
    """Charge the card for the postcard order and return the charge id."""
    amount = quantity * UNIT_PRICE + SHIPPING_COST
    amount += amount * TAX_RATE
    cents = int(amount * 100)
    try:
        logger.info("Charging customer $%.2f", amount)
        charge = stripe.Charge.create(
            amount=cents,
            currency="usd",
            source=token,
            description="Summer postcard order",
        )
        return charge.id
    except Exception as exc:  # broad for demo
        logger.error("Payment failed: %s", exc)
        raise PaymentError(str(exc)) from exc
