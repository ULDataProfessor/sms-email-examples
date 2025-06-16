"""Clean raw CSV data and output a normalized file."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT_FILE = Path("raw_data.csv")
OUTPUT_FILE = Path("cleaned.csv")


def clean(csv_path: Path = INPUT_FILE, out_path: Path = OUTPUT_FILE) -> None:
    df = pd.read_csv(csv_path)
    thresh = int(df.shape[1] * 0.8)
    df = df.dropna(thresh=thresh)
    date_cols = [c for c in df.columns if c.startswith("date_")]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
    df = df.drop_duplicates(subset=["id", "timestamp"], keep="first")
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    clean()
