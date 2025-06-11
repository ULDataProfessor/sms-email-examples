"""Persist order info to SQLite."""

import os
import sqlite3
from pathlib import Path
from typing import Dict

from .config import logger

DB_PATH = Path(os.getenv("DB_PATH", "orders.db"))

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customer_email TEXT,
    address TEXT,
    design_url TEXT,
    print_order_id TEXT,
    charge_id TEXT,
    status TEXT
)
"""


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(CREATE_SQL)
    conn.commit()
    conn.close()


def save_order(record: Dict[str, str]) -> None:
    logger.debug("Saving order to %s", DB_PATH)
    fields = (
        record["customer_name"],
        record["customer_email"],
        record["address"],
        record["design_url"],
        record["print_order_id"],
        record["charge_id"],
        record["status"],
    )
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO orders (customer_name, customer_email, address, design_url, print_order_id, charge_id, status)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        fields,
    )
    conn.commit()
    conn.close()
