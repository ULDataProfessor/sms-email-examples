---
---

# 📊 Accounting Firm AI Pipeline Example

`pipeline.py` demonstrates a minimal invoice processing workflow. It reads a CSV of invoices, identifies those that remain unpaid, generates reminder messages, and prints them.

## Sample CSV format
```
client,amount,paid
Acme,500,no
Foo Corp,300,yes
```

## Running
```bash
python pipeline.py
```
Specify the path to your invoice CSV when prompted.
