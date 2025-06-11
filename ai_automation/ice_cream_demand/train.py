"""Train an XGBoost model to forecast ice cream demand."""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from xgboost import XGBRegressor

from prepare_data import prepare_dataset, FEATURES

MODEL_PATH = Path("model.pkl")
HISTORY_PATH = Path("history.csv")


def train_model(csv_path: str | Path) -> None:
    df = prepare_dataset(csv_path)
    df = df.sort_values("date")
    X = df[FEATURES]
    y = df["units_sold"]
    model = XGBRegressor(objective="reg:squarederror", n_estimators=200)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    df.tail(7).to_csv(HISTORY_PATH, index=False)
    print("Model saved to", MODEL_PATH)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python train.py sales.csv")
        sys.exit(1)
    train_model(sys.argv[1])
