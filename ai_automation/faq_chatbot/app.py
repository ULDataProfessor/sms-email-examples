"""FastAPI app exposing a FAQ chatbot endpoint."""

from fastapi import FastAPI
from pydantic import BaseModel

from .embeddings import FAQIndexer

indexer = FAQIndexer()
app = FastAPI(title="FAQ Chatbot")

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask(data: Question):
    """Return answers to the most similar FAQs."""
    results = indexer.query(data.question)
    answers = [r["answer"] for r in results]
    return {"answers": answers}
