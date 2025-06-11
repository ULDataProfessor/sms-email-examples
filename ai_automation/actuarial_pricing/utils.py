"""Utility helpers for logging and exceptions."""

import logging


class PricingError(Exception):
    """Base class for pricing related errors."""


class DataLoadError(PricingError):
    """Raised when input data cannot be loaded."""


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging for the package."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
