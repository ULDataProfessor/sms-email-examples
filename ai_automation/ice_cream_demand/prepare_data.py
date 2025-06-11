"""Merge sales with weather and engineer features."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

import pandas as pd
import holidays

from fetch_weather import fetch_weather

FEATURES = [
    "lag1",
    "lag7",
    "day_of_week",
    "is_holiday",
    "temperature",
    "precipitation",
    "temp_weekend",
]


def _load_sales(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def _fetch_weather_for_sales(df: pd.DataFrame) -> pd.DataFrame:
    start = df["date"].min().strftime("%Y-%m-%d")
    end = df["date"].max().strftime("%Y-%m-%d")
    frames = [fetch_weather(start, end, loc) for loc in df["location"].unique()]
    weather = pd.concat(frames)
    return df.merge(weather, on=["date", "location"], how="left")


def _add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["location", "product", "date"])
    df["lag1"] = df.groupby(["product", "location"])["units_sold"].shift(1)
    df["lag7"] = df.groupby(["product", "location"])["units_sold"].shift(7)
    df["day_of_week"] = df["date"].dt.dayofweek
    us_holidays = holidays.US()
    df["is_holiday"] = df["date"].dt.date.isin(us_holidays)
    df["is_weekend"] = df["day_of_week"] >= 5
    df["temp_weekend"] = df["temperature"] * df["is_weekend"]
    df = df.dropna(subset=["lag1", "lag7"])
    return df


def prepare_dataset(csv_path: str | Path) -> pd.DataFrame:
    sales = _load_sales(Path(csv_path))
    merged = _fetch_weather_for_sales(sales)
    return _add_features(merged)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prepare_data.py sales.csv")
        sys.exit(1)
    prepared = prepare_dataset(sys.argv[1])
    prepared.to_csv("prepared.csv", index=False)
    print("Prepared data written to prepared.csv")
