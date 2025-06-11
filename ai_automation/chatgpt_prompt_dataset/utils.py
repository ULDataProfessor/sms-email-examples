import logging
from typing import Any, Dict

import openai
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

logger = logging.getLogger(__name__)


def build_payload(description: str) -> Dict[str, Any]:
    """Construct the ChatCompletion payload for a scenario description."""
    return {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an expert business analyst."},
            {"role": "user", "content": description},
        ],
        "temperature": 0.7,
    }


@retry(
    retry=retry_if_exception_type(openai.error.RateLimitError),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
def chat_completion_with_retry(payload: Dict[str, Any]) -> Any:
    """Call the OpenAI API with retry logic for rate limits."""
    try:
        return openai.ChatCompletion.create(**payload)
    except openai.error.RateLimitError as e:
        logger.warning("Rate limit hit: %s. Retrying...", e)
        raise

