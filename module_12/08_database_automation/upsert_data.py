"""Load CSV data and upsert into PostgreSQL."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

CSV_PATH = Path("data.csv")


def get_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )


def upsert_csv(csv_file: Path = CSV_PATH) -> None:
    df = pd.read_csv(csv_file)
    cols = list(df.columns)
    placeholders = ",".join(["%s"] * len(cols))
    update_clause = ", ".join(f"{c}=EXCLUDED.{c}" for c in cols if c != "id")
    sql = f"INSERT INTO public.data_table ({','.join(cols)}) VALUES ({placeholders}) " \
          f"ON CONFLICT (id) DO UPDATE SET {update_clause}"

    conn = get_connection()
    cur = conn.cursor()

    for start in range(0, len(df), 100):
        batch = df.iloc[start : start + 100]
        execute_batch(cur, sql, batch.values.tolist())
        conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    upsert_csv()
