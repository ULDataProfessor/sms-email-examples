# Sora TTS Dataset Builder

This folder contains a small package for generating a text-to-speech dataset using the **Sora** API.

## Voice styles

The API supports multiple voices. Typical styles include `narrator`, `conversational`, and `energetic`. Each block in the JSON input selects a style with the `voice_style` field.

## Running

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the environment variable `SORA_API_KEY` with your API key.
3. Provide a JSON file containing objects like:
   ```json
   [
     {"id": "promo1", "text": "Sale starts today", "voice_style": "narrator"},
     {"id": "promo2", "text": "Don't miss out", "voice_style": "energetic"}
   ]
   ```
4. Run the builder:
   ```bash
   python -m sora_tts_dataset.build marketing_copy.json output_dir
   ```

The script saves MP3 files and writes `sora_dataset.csv` with the metadata.

## Error handling and rate limits

API errors are raised if a request fails. When a `429` status code is returned, the script waits for the `Retry-After` time before retrying the request.

## Verifying durations

The duration of each clip is taken from the `X-Duration-Seconds` response header. This value is recorded in the CSV so you can confirm audio lengths after download.
