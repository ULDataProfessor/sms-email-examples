"""Batch avatar generation using HeyGen API."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import requests

from poller import Poller

API_BASE_URL = os.getenv("HEYGEN_API_BASE_URL", "https://api.heygen.com")
API_KEY = os.getenv("HEYGEN_API_KEY")
OUTPUT_DIR = Path("output")
LOG_FILE = Path("generation_log.csv")


def create_avatar(template: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Call HeyGen create avatar endpoint."""
    url = f"{API_BASE_URL}/v1/avatar/create"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(url, headers=headers, json={"template": template, "metadata": metadata})
    response.raise_for_status()
    return response.json()


def download_video(video_url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(video_url)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)


def process_excel(path: str, interval: int = 5, timeout: int = 300) -> None:
    df = pd.read_excel(path)
    poller = Poller(interval=interval, timeout=timeout)

    with open(LOG_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user_id", "timestamp", "status", "video_url"])

        for _, row in df.iterrows():
            user_id = row["user_id"]
            name = row.get("name", "")
            template = row["avatar_template"]

            meta = {"name": name, "user_id": user_id}
            creation = create_avatar(template, meta)
            status_url = creation.get("status_url")

            result = poller.poll(lambda: requests.get(status_url, headers={"Authorization": f"Bearer {API_KEY}"}))
            video_url = result.get("video_url")
            download_video(video_url, OUTPUT_DIR / f"{user_id}.mp4")
            writer.writerow([user_id, result.get("completed_at"), result.get("status"), video_url])


if __name__ == "__main__":
    excel_path = input("Path to Excel roster: ")
    process_excel(excel_path)
