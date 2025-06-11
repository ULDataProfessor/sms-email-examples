"""Payment processing using Stripe."""
import os
import stripe
from .config import logger
from .utils import PaymentError

stripe.api_key = os.getenv('STRIPE_API_KEY')
PRICE_CENTS = int(os.getenv('TSHIRT_PRICE_CENTS', '2000'))


def process_payment(token: str, amount: int = PRICE_CENTS, currency: str = 'usd') -> str:
    """Charge the payment token and return charge ID."""
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,
            description='T-shirt purchase',
        )
        return charge['id']
    except stripe.error.StripeError as exc:
        logger.exception("Payment failed")
        raise PaymentError(str(exc)) from exc
