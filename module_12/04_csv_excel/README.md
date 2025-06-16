# CSV & Excel Automation

## Project Overview
This example processes a sales CSV file and generates an Excel workbook containing both the raw data and a summary table. It demonstrates simple aggregation and export features using pandas.

## Variables
`CSV_FILE` identifies the input CSV while `OUTPUT_FILE` is the Excel file written by `process_sales.py`. Adjust these constants if your files live elsewhere or you want a different output name.

## Instructions
Install pandas with `pip install pandas` and place `sales.csv` in this directory. Running `python process_sales.py` will create `summary.xlsx` with two sheets: `raw` (the original data) and `summary` (total and average sales by region).

## Explanation
The script reads the CSV using `pandas.read_csv` and uses `groupby` to aggregate totals. `pandas.ExcelWriter` then writes both the raw and summarized data to a single workbook. This simple pattern can be adapted for more elaborate reporting tasks.
