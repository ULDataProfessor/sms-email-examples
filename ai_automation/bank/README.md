---
---

# 🏦 Bank AI Pipeline Example

This example illustrates a basic workflow for analyzing bank transactions. The script `pipeline.py` reads a CSV file of transactions, flags any that exceed $10,000, processes them into a short report, and prints the results.

## Sample CSV format
```
id,amount,account
1,5000,123
2,20000,456
```

## Running
```bash
python pipeline.py
```
You'll be prompted for the path to a CSV file containing your transaction data.
