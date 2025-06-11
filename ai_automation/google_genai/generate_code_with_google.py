import os

# Example of using Google Generative AI to produce a simple code snippet.
# This script uses the google.generativeai Python library (Gemini/PaLM models).
# You will need a valid API key from Google Cloud.

import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set")

# Configure the client with your API key
client = genai.Client(api_key=API_KEY)

prompt = (
    "Write a Python function that calculates the factorial of a number. "
    "Include docstrings and type hints."
)

response = client.generate_text(prompt=prompt, model="models/text-bison-001")

print(response.text)
