#!/usr/bin/env python3
"""Query images by label and confidence."""

import argparse
from pathlib import Path

from retail_image_classification.db import query_labels


def main() -> None:
    parser = argparse.ArgumentParser(description="Query labeled images")
    parser.add_argument("label", help="Label to search for")
    parser.add_argument("--min_confidence", type=float, default=90.0, help="Minimum confidence")
    parser.add_argument("--db", type=Path, default=Path("labels.db"), help="SQLite database path")
    args = parser.parse_args()

    rows = query_labels(args.label, args.min_confidence, args.db)
    if not rows:
        print("No matching images found")
    else:
        for row in rows:
            print(f"{row['filename']} ({row['confidence']:.2f}%)")


if __name__ == "__main__":
    main()
