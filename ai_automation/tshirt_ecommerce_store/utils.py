"""Utility functions and custom exceptions."""

class OrderError(Exception):
    """Base exception for order workflow."""

class DesignError(OrderError):
    """Raised when design generation fails."""

class PaymentError(OrderError):
    """Raised when payment processing fails."""

class ProductionError(OrderError):
    """Raised when production API call fails."""

class ShippingError(OrderError):
    """Raised when shipping tracking fails."""
