"""Utility classes and helpers."""

class PostcardError(Exception):
    """Base error for the postcard pipeline."""

class DesignError(PostcardError):
    """Raised when art generation fails."""

class PrintError(PostcardError):
    """Raised when the print API fails."""

class PaymentError(PostcardError):
    """Raised when payment processing fails."""

class NotificationError(PostcardError):
    """Raised when sending email fails."""
