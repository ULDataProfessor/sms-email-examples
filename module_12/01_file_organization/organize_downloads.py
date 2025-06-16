"""Organize files in Downloads folder by extension."""
from pathlib import Path
import shutil

EXTENSION_MAP = {
    ".txt": "text",
    ".md": "text",
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".pdf": "pdfs",
}


def organize_downloads(source: Path | None = None) -> None:
    """Move files into subfolders based on extension."""
    source = source or Path.home() / "Downloads"
    for item in source.iterdir():
        if not item.is_file():
            continue
        folder = EXTENSION_MAP.get(item.suffix.lower())
        if not folder:
            continue
        target_dir = source / folder
        target_dir.mkdir(exist_ok=True)
        destination = target_dir / item.name
        print(f"Moving {item.name} -> {destination}")
        shutil.move(str(item), destination)


if __name__ == "__main__":
    organize_downloads()
