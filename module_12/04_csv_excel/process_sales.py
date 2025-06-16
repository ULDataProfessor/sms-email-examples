"""Aggregate sales CSV data and export to Excel."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

CSV_FILE = "sales.csv"
OUTPUT_FILE = "summary.xlsx"


def generate_summary(csv_path: Path = Path(CSV_FILE), out_path: Path = Path(OUTPUT_FILE)) -> None:
    """Read a sales CSV, compute totals, and export to Excel."""
    df = pd.read_csv(csv_path)
    summary = (
        df.groupby("region")
        .agg(total=("amount", "sum"), average=("amount", "mean"))
        .reset_index()
    )
    with pd.ExcelWriter(out_path) as writer:
        df.to_excel(writer, sheet_name="raw", index=False)
        summary.to_excel(writer, sheet_name="summary", index=False)


if __name__ == "__main__":
    generate_summary()
