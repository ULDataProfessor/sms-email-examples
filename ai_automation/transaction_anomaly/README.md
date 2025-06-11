---
---

# 💳 Transaction Anomaly Detection Pipeline

This example shows a simple approach to flagging unusual transactions with Python.

## Feature engineering
- Transactions are sorted by `account_id` and `date`.
- A rolling window (default 5) computes the mean and standard deviation of `amount` per account.
- A z-score for each amount is derived from the rolling statistics.
- These features (`amount`, `rolling_mean`, `zscore`) feed the anomaly model.

## IsolationForest
- The detector relies on scikit-learn's `IsolationForest`.
- Key parameters include `contamination` (expected outlier fraction) and `random_state`.
- Adjust `contamination` to tune sensitivity; start around `0.01` for rare anomalies.

## CLI usage
Run the pipeline with:
```bash
python detect.py --mode batch --input transactions.csv
```

- **Batch** mode processes an entire CSV and outputs flagged rows to `anomaly_report.csv`.
- **Stream** mode appends new data to a history CSV specified by `--history` and only reports anomalies from the new portion.
- A summary CSV with basic statistics is written alongside the main report.

The CLI prints how many transactions were flagged and where the summary was saved.
