"""Utility functions for transaction anomaly detection."""

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.ensemble import IsolationForest


def load_transactions(path: str) -> pd.DataFrame:
    """Load transactions CSV with columns date, account_id, amount, merchant."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def feature_engineering(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Add rolling statistics and z-score features."""
    df = df.sort_values(["account_id", "date"]).copy()
    rolling = (
        df.groupby("account_id")["amount"]
        .rolling(window=window, min_periods=1)
        .agg(["mean", "std"])
        .reset_index(level=0, drop=True)
    )
    df["rolling_mean"] = rolling["mean"]
    df["rolling_std"] = rolling["std"].fillna(0)
    df["zscore"] = (df["amount"] - df["rolling_mean"]) / df["rolling_std"].replace(0, 1)
    return df


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.01) -> Tuple[pd.DataFrame, IsolationForest]:
    """Run IsolationForest and return dataframe with anomaly flag."""
    model = IsolationForest(contamination=contamination, random_state=42)
    features = df[["amount", "rolling_mean", "zscore"]].fillna(0)
    df = df.copy()
    df["anomaly"] = model.fit_predict(features) == -1
    return df, model
