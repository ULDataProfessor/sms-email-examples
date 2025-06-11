import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

from forecast import read_history, forecast_depletion, SAFETY_LEVEL
from logger import init_db, log_reorder

load_dotenv()

API_URL = os.environ.get("SUPPLIER_API_URL", "http://supplier.example.com")
API_TOKEN = os.environ.get("SUPPLIER_API_TOKEN", "")
SAFETY_LEVEL = int(os.environ.get("SAFETY_LEVEL", SAFETY_LEVEL))


def place_order(sku: str, quantity: int) -> requests.Response:
    url = f"{API_URL.rstrip('/')}/orders"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {"sku": sku, "quantity": quantity}
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    return response


def process(csv_path: Path) -> pd.DataFrame:
    df = read_history(csv_path)
    forecast_df = forecast_depletion(df)

    init_db()

    for _, row in forecast_df.iterrows():
        if row["predicted_stock"] < SAFETY_LEVEL:
            reorder_qty = int(SAFETY_LEVEL * 2 - row["predicted_stock"])
            try:
                resp = place_order(row["item_id"], reorder_qty)
                success = resp.status_code == 201
                log_reorder(
                    row["item_id"],
                    reorder_qty,
                    resp.status_code,
                    resp.text,
                    success,
                )
            except Exception as exc:
                log_reorder(
                    row["item_id"],
                    reorder_qty,
                    None,
                    None,
                    False,
                    error=str(exc),
                )
    return forecast_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto reorder pipeline")
    parser.add_argument("csv_path", type=Path, help="Path to POS CSV")
    args = parser.parse_args()

    process(args.csv_path)
