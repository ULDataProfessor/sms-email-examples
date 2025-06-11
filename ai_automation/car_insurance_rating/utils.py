"""Utility helpers for logging and custom exceptions."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .config import LOG_FILE

# Configure logger
logger = logging.getLogger("car_insurance")
logger.setLevel(logging.INFO)

_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
_handler.setFormatter(_formatter)
logger.addHandler(_handler)


class ExternalAPIError(Exception):
    """Raised when an external API call fails."""


class RatingError(Exception):
    """Raised when premium calculation fails."""
