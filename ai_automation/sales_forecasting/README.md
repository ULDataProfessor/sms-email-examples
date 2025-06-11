# Sales Forecasting Example

This folder contains a minimal example of forecasting daily sales using Python.
The example demonstrates how to transform raw sales data, train a forecasting
model, and visualize the results.

## Files

- `forecast.py` – Reads a CSV of historical daily sales and forecasts the next
  30 days using Prophet.
- `requirements.txt` – Python dependencies required to run the example.

## Time-Series Decomposition

Time-series data can be viewed as a combination of **trend**, **seasonality** and
**residual** components. Trend describes long‑term movement, seasonality captures
repeating patterns such as day‑of‑week effects, and residual represents random
noise. Prophet automatically models these pieces which makes it convenient for
business data like daily sales.

## Model Selection and Hyperparameter Tuning

The script uses Facebook's Prophet library, which generally performs well on
daily business metrics. Prophet supports parameters such as `seasonality_mode`
(additive vs. multiplicative) and `changepoint_prior_scale` that control how the
trend adapts to changes. These can be tuned by fitting the model with different
values and evaluating hold‑out performance (MAE/MAPE in this example).

You can also experiment with ARIMA models from the `statsmodels` library by
modifying `forecast.py` if Prophet does not provide satisfactory accuracy.

## Running the Forecast

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare a CSV file containing columns `date`, `store_id`, and `sales`.
3. Run the script:
   ```bash
   python forecast.py path/to/sales.csv --store-id 1 --plot forecast.png
   ```
   The program prints MAE and MAPE for the last 30 days and saves a plot showing
   historical sales together with the 30‑day forecast.

The resulting chart helps you visually compare actual sales to the predicted
values and understand future expectations.
