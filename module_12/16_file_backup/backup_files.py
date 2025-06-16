"""Copy files from source to backup directory."""
from __future__ import annotations

from pathlib import Path
import shutil

SOURCE_DIR = Path("source")
BACKUP_DIR = Path("backup")


def backup(source: Path = SOURCE_DIR, dest: Path = BACKUP_DIR) -> None:
    dest.mkdir(exist_ok=True)
    for file in source.iterdir():
        if file.is_file():
            shutil.copy2(file, dest / file.name)


if __name__ == "__main__":
    backup()
