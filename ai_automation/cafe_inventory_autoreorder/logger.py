import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "reorder_log.db"


def init_db(db_path: Path = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reorder_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            item_id TEXT,
            quantity INTEGER,
            status_code INTEGER,
            response_body TEXT,
            success INTEGER,
            error TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def log_reorder(
    item_id: str,
    quantity: int,
    status_code: Optional[int],
    response_body: Optional[str],
    success: bool,
    error: Optional[str] = None,
    db_path: Path = DB_PATH,
) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reorder_log (timestamp, item_id, quantity, status_code, response_body, success, error) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.utcnow().isoformat(),
            item_id,
            quantity,
            status_code,
            response_body,
            int(success),
            error,
        ),
    )
    conn.commit()
    conn.close()
