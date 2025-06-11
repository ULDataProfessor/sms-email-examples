# Cafe Inventory Auto-Reorder

This folder contains a small pipeline that forecasts inventory depletion for a cafe and automatically places reorders with a supplier API.

## Files

- `forecast.py` – loads POS history and predicts daily sales using exponential smoothing.
- `reorder.py` – checks forecasts against a safety level and posts reorders to the supplier API while logging each attempt.
- `logger.py` – creates a SQLite `reorder_log.db` and stores API responses.
- `report.py` – emails a daily summary of reorder activity and predicted stock-out dates.
- `requirements.txt` – Python dependencies.

## Forecasting

`forecast.py` uses `statsmodels` `SimpleExpSmoothing` to estimate the next day's sales for each SKU. The forecast is projected 14 days forward. By default the safety stock level is **10 units** but can be overridden with the `SAFETY_LEVEL` environment variable.

A reorder is triggered when the forecasted stock after 14 days falls below the safety level. The reorder amount brings inventory back to roughly twice the safety level.

## Supplier API

Set the following environment variables in a `.env` file:

```
SUPPLIER_API_URL=https://supplier.example.com
SUPPLIER_API_TOKEN=your_token_here
SAFETY_LEVEL=10
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
EMAIL_USER=bot@example.com
EMAIL_PASS=password
EMAIL_TO=manager@example.com
```

`reorder.py` POSTs to `$SUPPLIER_API_URL/orders` with JSON:

```json
{ "sku": "ABC123", "quantity": 20 }
```

The token is sent as a bearer token in the `Authorization` header.

## Running Daily

Install dependencies and run the pipeline with the latest POS CSV:

```bash
pip install -r requirements.txt
python reorder.py path/to/daily_pos.csv
```

To run automatically each day, create a cron entry similar to:

```
0 2 * * * /usr/bin/python /path/to/reorder.py /data/pos_$(date +\%Y-\%m-\%d).csv >> /var/log/reorder.log 2>&1
```

## Reorder Log

All API calls are stored in `reorder_log.db` in the same folder. Inspect the log with:

```bash
sqlite3 reorder_log.db "SELECT * FROM reorder_log ORDER BY timestamp DESC LIMIT 20;"
```

Run `report.py` after the pipeline to send the daily email summary.
