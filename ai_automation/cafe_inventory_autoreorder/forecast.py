from datetime import date, timedelta
from pathlib import Path
from typing import Dict

import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


SAFETY_LEVEL = 10  # default safety stock if not overridden


def read_history(path: Path) -> pd.DataFrame:
    """Load POS history CSV (item_id, sold_qty, current_stock[, date])."""
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


def forecast_depletion(df: pd.DataFrame, days: int = 14) -> pd.DataFrame:
    """Return forecasted daily demand and stockout date for each SKU."""
    results = []
    today = date.today()
    for item_id, group in df.groupby("item_id"):
        group = group.sort_index()
        sales = group["sold_qty"].astype(float)
        current_stock = group["current_stock"].iloc[-1]
        if len(sales) < 2:
            daily = sales.iloc[-1]
        else:
            model = SimpleExpSmoothing(sales, initialization_method="heuristic")
            fit = model.fit()
            daily = float(fit.forecast(1).iloc[0])
        predicted_stock = current_stock - daily * days
        days_to_oos = current_stock / daily if daily > 0 else float("inf")
        stockout_date = today + timedelta(days=int(days_to_oos)) if daily > 0 else None
        results.append(
            {
                "item_id": item_id,
                "predicted_daily_sales": daily,
                "predicted_stock": predicted_stock,
                "stockout_date": stockout_date,
            }
        )
    return pd.DataFrame(results)
