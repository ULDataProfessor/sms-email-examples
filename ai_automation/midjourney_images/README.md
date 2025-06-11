# Midjourney Image Generation Example

This folder shows a basic approach to calling a Midjourney-style API to create images.

Midjourney itself does not offer an official API. Some third-party services expose a compatible endpoint, so this example uses a generic HTTP request.

## File

- `generate_image_midjourney.py` – Sends a prompt to an API URL and prints the image URL returned by the service.

## Usage

1. Install the `requests` library.
2. Set the `MIDJOURNEY_API_URL` and `MIDJOURNEY_API_KEY` environment variables.
3. Run the script:
   ```bash
   python generate_image_midjourney.py
   ```

The script posts a prompt describing a futuristic city and prints the URL of the generated image.
