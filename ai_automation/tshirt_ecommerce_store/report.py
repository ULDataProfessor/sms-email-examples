"""Order reporting module using SQLite."""
import sqlite3
import os
from pathlib import Path
from .config import logger

DB_PATH = Path(os.getenv('DB_PATH', 'orders.db'))


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_email TEXT,
            design_url TEXT,
            charge_id TEXT,
            production_id TEXT,
            tracking_url TEXT
        )"""
    )
    conn.commit()
    conn.close()


def save_order(customer: dict, design_url: str, charge_id: str, production_id: str, tracking_url: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (customer_name, customer_email, design_url, charge_id, production_id, tracking_url) VALUES (?, ?, ?, ?, ?, ?)",
        (customer['name'], customer['email'], design_url, charge_id, production_id, tracking_url),
    )
    order_id = cur.lastrowid
    conn.commit()
    conn.close()
    logger.info('Saved order %s', order_id)
    return order_id
