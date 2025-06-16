"""Utilities for fetching data from an API and SQLite database."""
from __future__ import annotations

import sqlite3
from typing import Any, Dict, List

import pandas as pd
import requests

API_URL = "https://api.example.com/data"
DB_PATH = "data.db"


def fetch_api_data(url: str = API_URL) -> List[Dict[str, Any]]:
    """GET JSON data from a REST API."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_db_data(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieve rows from a SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT * FROM data")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


def combine_data(api_data: List[Dict[str, Any]], db_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Merge API and DB records into one DataFrame."""
    df_api = pd.DataFrame(api_data)
    df_db = pd.DataFrame(db_data)
    return pd.concat([df_api, df_db], ignore_index=True)


if __name__ == "__main__":
    api_records = fetch_api_data()
    db_records = fetch_db_data()
    df = combine_data(api_records, db_records)
    print(df.head())
