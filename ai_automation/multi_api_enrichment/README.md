# Multi-API Enrichment Example

This folder demonstrates chaining several APIs to enrich product descriptions with marketing headlines, audio, and images.

## Files

- `enrich.py` – Asynchronously generates headlines with OpenAI and requests audio and images from remote APIs.
- `async_utils.py` – Helper for running coroutines under a concurrency limit with simple retry backoff.
- `requirements.txt` – Python dependencies.

## Chaining API Outputs

Each product's description feeds into OpenAI to create a headline. That headline then becomes the input text for both a text‑to‑speech API (Sora) and an image generation API (Midjourney). The headline itself is written to `enriched.csv` while the audio and image are stored under the `audio/` and `images/` directories.

## Concurrency and Backoff

The `async_utils.rate_limited_gather` function wraps `asyncio.gather` with a semaphore to limit in‑flight requests. When network calls fail, tasks wait for an exponentially increasing delay before retrying. This keeps the overall request rate under control while handling transient errors.

## File Naming

Output media files use the product ID so they are easy to match back to the source record:

```
audio/<product_id>.mp3
images/<product_id>.png
```

The CSV `enriched.csv` will contain the original product columns plus a new `headline` column.
