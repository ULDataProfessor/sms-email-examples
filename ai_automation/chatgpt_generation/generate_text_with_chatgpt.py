import os
import openai

# Example using the OpenAI API (ChatGPT) to generate text.
# Requires the openai package and a valid API key in OPENAI_API_KEY.

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

prompt = "Explain the concept of recursion in Python in two sentences."

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message["content"].strip())
