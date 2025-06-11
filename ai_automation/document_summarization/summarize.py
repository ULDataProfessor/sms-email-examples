"""Generate document summaries using OpenAI's ChatCompletion API."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

import openai
import pandas as pd

# Approximate number of characters to send in each API call.
CHUNK_SIZE = 2000

SYSTEM_PROMPT = "Provide a concise executive summary for the given text."


def load_documents(directory: Path) -> List[Path]:
    """Return a list of text files in the given directory."""
    return [p for p in directory.glob("*.txt") if p.is_file()]


def split_text(text: str, size: int = CHUNK_SIZE) -> List[str]:
    """Split text into character-based chunks."""
    return [text[i : i + size] for i in range(0, len(text), size)]


def summarize(text: str) -> str:
    """Summarize a single chunk using the ChatCompletion API."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()


def summarize_document(path: Path, out_dir: Path) -> pd.Series:
    """Summarize one document and save markdown outputs."""
    text = path.read_text()
    chunks = split_text(text)

    chunk_summaries = [summarize(c) for c in chunks]
    final_summary = summarize("\n\n".join(chunk_summaries))

    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{path.stem}.md").write_text(text)
    (out_dir / f"{path.stem}_summary.md").write_text(final_summary)

    return pd.Series({"file": path.name, "summary": final_summary})


def main() -> None:
    doc_dir = Path(input("Directory of text files: ").strip())
    out_dir = Path(input("Output directory [summaries]: ").strip() or "summaries")

    results = [summarize_document(p, out_dir) for p in load_documents(doc_dir)]
    df = pd.DataFrame(results)
    print(df)


if __name__ == "__main__":
    main()
