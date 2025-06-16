"""Batch convert images to grayscale."""
from __future__ import annotations

from pathlib import Path
from PIL import Image

SOURCE_DIR = Path("images")
OUTPUT_DIR = Path("output")


def convert_images(source: Path = SOURCE_DIR, dest: Path = OUTPUT_DIR) -> None:
    dest.mkdir(exist_ok=True)
    for img_path in source.glob("*.jpg"):
        with Image.open(img_path) as img:
            gray = img.convert("L")
            gray.save(dest / img_path.name)


if __name__ == "__main__":
    convert_images()
