"""Enrich product descriptions with headlines, audio, and images."""

import os
import asyncio
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import aiohttp
import openai

from async_utils import rate_limited_gather

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SORA_API_URL = os.getenv("SORA_API_URL")
MIDJOURNEY_API_URL = os.getenv("MIDJOURNEY_API_URL")
MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY")

openai.api_key = OPENAI_API_KEY

AUDIO_DIR = Path("audio")
IMAGE_DIR = Path("images")

AUDIO_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

async def create_headline(text: str) -> str:
    """Use OpenAI to create a short marketing headline."""
    resp = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You write punchy marketing headlines."},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content.strip()

async def fetch_audio(session: aiohttp.ClientSession, product_id: str, text: str) -> None:
    """Request text-to-speech audio and save to disk."""
    async with session.post(SORA_API_URL, json={"text": text}) as resp:
        content = await resp.read()
    (AUDIO_DIR / f"{product_id}.mp3").write_bytes(content)

async def fetch_image(session: aiohttp.ClientSession, product_id: str, prompt: str) -> None:
    """Request an image from Midjourney-compatible API and save to disk."""
    payload = {"prompt": prompt, "api_key": MIDJOURNEY_API_KEY}
    async with session.post(MIDJOURNEY_API_URL, json=payload) as resp:
        content = await resp.read()
    (IMAGE_DIR / f"{product_id}.png").write_bytes(content)

async def process_product(session: aiohttp.ClientSession, row: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a single product record."""
    product_id = str(row["product_id"])
    text = str(row["text"])
    headline = await create_headline(text)
    await asyncio.gather(
        fetch_audio(session, product_id, headline),
        fetch_image(session, product_id, headline),
    )
    return {"product_id": product_id, "headline": headline}

async def main(csv_path: str = "products.csv") -> None:
    df = pd.read_csv(csv_path)

    async with aiohttp.ClientSession() as session:
        tasks = [lambda row=row: process_product(session, row) for _, row in df.iterrows()]
        results = await rate_limited_gather(tasks, limit=3)

    result_df = pd.DataFrame(results)
    merged = df.merge(result_df, on="product_id")
    merged.to_csv("enriched.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main())
