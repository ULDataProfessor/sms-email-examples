# ChatGPT Prompt Dataset Builder

This folder demonstrates how to turn a spreadsheet of business scenarios into a dataset of prompts and ChatGPT responses.

## Files
- `generate.py` – reads scenarios and writes the resulting dataset.
- `utils.py` – helper functions for payload creation and retry logic.
- `requirements.txt` – dependencies (`openai`, `pandas`, `tenacity`).

## Input CSV Format
The input file must include the columns `scenario_id`, `description`, and `tone`. Example:

```
scenario_id,description,tone
1,"Analyze the market for winter coats","formal"
2,"Suggest a slogan for a family restaurant","friendly"
```

## Usage
Install the requirements and set your OpenAI API key:

```
pip install -r requirements.txt
export OPENAI_API_KEY=YOUR_KEY
python generate.py scenarios.csv dataset.csv
```

For each scenario the script builds a payload for OpenAI's ChatCompletion API and captures the assistant reply. The resulting `dataset.csv` contains the columns `scenario_id`, `prompt`, `response`, and `tokens_used`.

## Token Usage and Errors
The `tokens_used` column is populated from the API response's `usage.total_tokens` field. Rate-limit errors are logged, and the request is retried with exponential backoff. If a call ultimately fails, an exception is raised and the logs will indicate the error.
