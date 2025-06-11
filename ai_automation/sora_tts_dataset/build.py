"""Build an audio dataset using the Sora TTS API."""

import argparse
import json
import os
import time
from typing import List, Dict

import pandas as pd
import requests

from .config import load_api_key

TTS_URL = "https://api.sora.com/v1/tts"


def load_copy(path: str) -> List[Dict[str, str]]:
    """Load marketing copy blocks from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def synthesize(copy_blocks: List[Dict[str, str]], output_dir: str) -> pd.DataFrame:
    """Synthesize audio for each copy block and return metadata."""
    api_key = load_api_key()
    os.makedirs(output_dir, exist_ok=True)
    session = requests.Session()
    headers = {"Authorization": f"Bearer {api_key}"}
    rows = []

    for block in copy_blocks:
        text = block.get("text", "")
        voice = block.get("voice_style", "default")
        payload = {"text": text, "voice": voice}
        while True:
            resp = session.post(TTS_URL, json=payload, headers=headers)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", "1"))
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                raise RuntimeError(f"API error {resp.status_code}: {resp.text}")
            break
        file_name = f"{block.get('id')}_{voice}.mp3"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(resp.content)
        duration = float(resp.headers.get("X-Duration-Seconds", 0))
        rows.append(
            {
                "id": block.get("id"),
                "voice_style": voice,
                "duration_sec": duration,
                "file_path": file_path,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(output_dir, "sora_dataset.csv"), index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Sora TTS dataset")
    parser.add_argument("json_path", help="Path to marketing copy JSON list")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=".",
        help="Directory to write MP3 files and metadata",
    )
    args = parser.parse_args()
    blocks = load_copy(args.json_path)
    synthesize(blocks, args.output_dir)


if __name__ == "__main__":
    main()
