# Google Generative AI Example

This folder demonstrates how to call Google's generative AI API to create code snippets.

## File

- `generate_code_with_google.py` – Uses the `google.generativeai` library to request a Python function from the API.

## Usage

1. Install the `google-generativeai` package.
2. Set the `GOOGLE_API_KEY` environment variable with your API key.
3. Run the script:
   ```bash
   python generate_code_with_google.py
   ```

The program sends a prompt asking for a factorial function and prints the AI-generated code.
