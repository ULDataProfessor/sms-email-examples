# Data Cleaning Automation

## Project Overview
`clean_data.py` cleans a CSV file by removing records with many missing values, normalizing date columns and deduplicating rows. The result is written to a new file for further analysis.

## Variables
`INPUT_FILE` and `OUTPUT_FILE` define the paths of the source and cleaned CSVs. Any columns beginning with `date_` are treated as dates and converted to `YYYY-MM-DD` format.

## Instructions
Install pandas with `pip install pandas` and run `python clean_data.py`. The cleaned data will appear in `cleaned.csv` in the same directory.

## Explanation
The script calculates a threshold based on the number of columns and drops rows that do not meet it. It then uses `pandas.to_datetime` to parse date columns and finally removes duplicates using the `id` and `timestamp` fields.
