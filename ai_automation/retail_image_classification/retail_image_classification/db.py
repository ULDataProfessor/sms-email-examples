import sqlite3
import pandas as pd
from pathlib import Path
from typing import Iterable, Any


def init_db(db_path: Path) -> None:
    """Initialize the SQLite database with the required table."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS image_labels (
            filename TEXT,
            label TEXT,
            confidence REAL
        )
        """
    )
    conn.commit()
    conn.close()


def save_labels(df: pd.DataFrame, db_path: Path) -> None:
    """Save DataFrame records to the database."""
    conn = sqlite3.connect(db_path)
    df.to_sql("image_labels", conn, if_exists="append", index=False)
    conn.close()


def query_labels(label: str, min_confidence: float, db_path: Path) -> Iterable[sqlite3.Row]:
    """Query images that match the label and confidence threshold."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        "SELECT filename, label, confidence FROM image_labels WHERE label = ? AND confidence >= ?",
        (label, min_confidence),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
