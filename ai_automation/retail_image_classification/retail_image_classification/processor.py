from pathlib import Path
from typing import List, Dict

import boto3
import pandas as pd

from .db import init_db, save_labels


def detect_labels(image_path: Path, client, max_labels: int = 10) -> List[Dict]:
    """Call AWS Rekognition to detect labels for a given image."""
    with image_path.open("rb") as f:
        img_bytes = f.read()

    response = client.detect_labels(Image={"Bytes": img_bytes}, MaxLabels=max_labels)
    records = []
    for label in response.get("Labels", []):
        records.append({
            "filename": image_path.name,
            "label": label["Name"],
            "confidence": label["Confidence"],
        })
    return records


def process_folder(folder: Path, db_path: Path, confidence_threshold: float = 50.0) -> pd.DataFrame:
    """Process all images in a folder and store results in a SQLite database."""
    init_db(db_path)
    client = boto3.client("rekognition")
    all_records: List[Dict] = []

    for img_file in folder.iterdir():
        if img_file.is_file():
            for rec in detect_labels(img_file, client):
                if rec["confidence"] >= confidence_threshold:
                    all_records.append(rec)

    df = pd.DataFrame(all_records)
    if not df.empty:
        save_labels(df, db_path)
    return df
