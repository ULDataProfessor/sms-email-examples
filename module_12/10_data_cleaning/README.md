# Data Cleaning Automation

**Objective:**  
Automate cleaning of `raw_data.csv`:
- Remove rows with more than 20% missing values
- Standardize date columns to ISO format
- Deduplicate on a composite key

**Codex Prompt:**  
“Write a Python script using Pandas that loads `raw_data.csv`, drops rows with >20% NA, converts any `date_` columns to ISO (`YYYY-MM-DD`), removes duplicate rows based on `id` and `timestamp`, and writes cleaned data to `cleaned.csv`.”
