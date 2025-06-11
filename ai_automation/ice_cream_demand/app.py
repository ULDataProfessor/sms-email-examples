"""FastAPI service providing a 7-day demand forecast."""

from __future__ import annotations

from datetime import datetime, timedelta

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
import holidays

from fetch_weather import fetch_weather
from prepare_data import FEATURES

MODEL_PATH = "model.pkl"
HISTORY_PATH = "history.csv"

app = FastAPI()
model = joblib.load(MODEL_PATH)
history = pd.read_csv(HISTORY_PATH)
history["date"] = pd.to_datetime(history["date"])
location = history["location"].iloc[-1]
us_holidays = holidays.US()


@app.get("/forecast")
def forecast(date: str):
    try:
        start = pd.to_datetime(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")

    df = history.copy()
    preds: list[float] = []
    for i in range(7):
        day = start + timedelta(days=i)
        weather = fetch_weather(day.strftime("%Y-%m-%d"), day.strftime("%Y-%m-%d"), location).iloc[0]
        row = {
            "lag1": df["units_sold"].iloc[-1],
            "lag7": df["units_sold"].iloc[-7],
            "day_of_week": day.dayofweek,
            "is_holiday": day.date() in us_holidays,
            "temperature": weather["temperature"],
            "precipitation": weather["precipitation"],
        }
        row["temp_weekend"] = row["temperature"] * (row["day_of_week"] >= 5)
        pred = float(model.predict(pd.DataFrame([row])[FEATURES])[0])
        preds.append(pred)
        df = pd.concat([df, pd.DataFrame([{"date": day, "units_sold": pred}])], ignore_index=True)
    return {"date": date, "predicted_units": preds}
