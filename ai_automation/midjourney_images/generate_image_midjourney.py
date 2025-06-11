import os
import requests

# Example of sending a prompt to a Midjourney-like API to generate an image.
# Midjourney does not have an official public API. This sample illustrates how
# you might call a third-party service that exposes Midjourney functionality.

API_URL = os.getenv("MIDJOURNEY_API_URL")  # e.g. https://api.midjourney-proxy.xyz/imagine
API_KEY = os.getenv("MIDJOURNEY_API_KEY")

if not API_URL or not API_KEY:
    raise EnvironmentError("MIDJOURNEY_API_URL and MIDJOURNEY_API_KEY must be set")

prompt = "A futuristic city skyline at sunset"

response = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"prompt": prompt}
)

response.raise_for_status()

# The API might return a URL to the generated image
result = response.json()
print("Image URL:", result.get("image_url"))
