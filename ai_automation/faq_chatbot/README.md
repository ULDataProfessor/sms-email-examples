# FAQ Chatbot Example

This folder demonstrates a simple FAQ chatbot built with FastAPI. The app loads
questions and answers from `faq.csv`, indexes the questions with a
SentenceTransformers model, and exposes an `/ask` endpoint that returns the most
relevant answers for a user query.

## Embedding model

- **Model:** `all-MiniLM-L6-v2`
- **Similarity threshold:** `0.5`

Any FAQ whose cosine similarity score is below the threshold is filtered out.

## Retraining

When you add new questions to `faq.csv`, restart the server to rebuild the
embeddings. The `FAQIndexer` class automatically reloads the CSV on startup.

## Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API with uvicorn:
   ```bash
   uvicorn ai_automation.faq_chatbot.app:app --reload
   ```

## Usage example

Ask a question with curl:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "How can I track my order?"}' \
     http://localhost:8000/ask
```
Example response:
```json
{"answers": ["Use the tracking link in your confirmation email."]}
```
