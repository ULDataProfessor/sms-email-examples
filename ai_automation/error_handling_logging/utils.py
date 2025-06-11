class PipelineError(Exception):
    """Base class for pipeline exceptions."""

class ValidationError(PipelineError):
    """Raised when input data fails validation."""

class APIError(PipelineError):
    """Raised when an external API call fails."""

class ProcessingError(PipelineError):
    """Raised when the processing step fails."""
