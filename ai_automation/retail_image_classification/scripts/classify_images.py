#!/usr/bin/env python3
"""Process a folder of images and store label metadata in a SQLite database."""

import argparse
from pathlib import Path

from retail_image_classification.processor import process_folder


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify product images with AWS Rekognition")
    parser.add_argument("image_folder", type=Path, help="Folder containing product images")
    parser.add_argument("--db", type=Path, default=Path("labels.db"), help="SQLite database path")
    parser.add_argument("--min_confidence", type=float, default=50.0, help="Minimum confidence to store")
    args = parser.parse_args()

    df = process_folder(args.image_folder, args.db, args.min_confidence)
    if df.empty:
        print("No labels detected above the threshold")
    else:
        print(df)
        print(f"Saved {len(df)} records to {args.db}")


if __name__ == "__main__":
    main()
