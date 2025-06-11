import os


def load_api_key() -> str:
    """Return the Sora API key from the environment."""
    key = os.getenv("SORA_API_KEY")
    if not key:
        raise EnvironmentError("SORA_API_KEY environment variable not set")
    return key
