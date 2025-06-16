"""Generate a bar chart from CSV data."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path("data.csv")
OUTPUT_IMAGE = Path("chart.png")


def main(data_path: Path = DATA_FILE, out_path: Path = OUTPUT_IMAGE) -> None:
    df = pd.read_csv(data_path)
    grouped = df.groupby("category")[["value"]].sum()
    ax = grouped.plot(kind="bar")
    ax.figure.tight_layout()
    ax.figure.savefig(out_path)


if __name__ == "__main__":
    main()
