# Document Summarization Example

This folder demonstrates a small pipeline that creates executive summaries for a batch of text files using OpenAI's Chat API.

## Files

- `summarize.py` – reads `.txt` documents from a directory, splits each into manageable chunks, requests summaries from ChatGPT, assembles the results, and saves markdown files.
- `requirements.txt` – minimal dependencies (`openai`, `pandas`).

## Text-splitting logic and chunk size

Documents are divided into pieces of roughly **2000 characters**. This keeps each request well under the 4k token context window for `gpt-3.5-turbo` while leaving room for the prompt and summary. Adjust `CHUNK_SIZE` in `summarize.py` if your documents are significantly shorter or longer.

## Tuning the prompt

`summarize.py` uses the system prompt:

```
Provide a concise executive summary for the given text.
```

Edit `SYSTEM_PROMPT` in the script to request more detail or a different style of summary. For longer outputs, you can also increase the model's `max_tokens` parameter when calling the API.

## Running on a new batch

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=YOUR_KEY
   ```
3. Place your `.txt` files in a folder and run:
   ```bash
   python summarize.py
   ```
   The program will prompt for the location of the text files and an output directory. Each document's full text and final summary will be saved as markdown files in the output folder.
