# Ice Cream Demand Forecasting

This folder contains a small pipeline that merges historical ice cream sales with weather data to train a demand model and serve forecasts through a FastAPI service.

## Files

- `fetch_weather.py` – Downloads daily temperature and precipitation from the free [Open‑Meteo](https://open-meteo.com/) API.
- `prepare_data.py` – Merges sales with weather, adds lag features and calendar flags.
- `train.py` – Trains an XGBoost regressor and stores the model along with the last week of history.
- `app.py` – FastAPI application exposing `/forecast?date=YYYY-MM-DD`.
- `requirements.txt` – Python dependencies.

## Weather → Sales Features

The prepared dataset includes:

- `lag1`, `lag7` – Units sold 1 and 7 days prior.
- `day_of_week` – Numeric weekday indicator.
- `is_holiday` – Boolean flag using US public holidays.
- `temp_weekend` – Temperature multiplied by a weekend indicator.
- Raw daily `temperature` and `precipitation`.

These features capture short‑term trends and how warm weekends or holidays boost demand.

## Model and Hyperparameters

An `XGBRegressor` is trained with `objective="reg:squarederror"` and `n_estimators=200`. XGBoost handles nonlinear relationships and interactions between the engineered features.

## Running the Pipeline

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare a CSV `sales.csv` with columns `date`, `product`, `units_sold`, `location`.
3. Train the model:
   ```bash
   python train.py sales.csv
   ```
4. Start the API server:
   ```bash
   uvicorn app:app --reload
   ```
5. Request a forecast starting from a date:
   ```bash
   curl 'http://localhost:8000/forecast?date=2024-07-01'
   ```
   The response contains seven predicted `units_sold` values for the upcoming week.
