# Multi-Source Data Extraction

## Project Overview
`multi_source_data.py` collects data from a REST API and a local SQLite database. It provides helper functions to fetch records from each source and merge them into a unified pandas DataFrame.

## Variables
The script defines `API_URL` and `DB_PATH` as the default locations of the API endpoint and SQLite file. These variables can be passed to the functions if you need to target a different API or database.

## Instructions
Install the required libraries with `pip install pandas requests`. Then run `python multi_source_data.py` to fetch the API data, read the SQLite table and display the combined output. You may also import the module and call `fetch_api_data` or `fetch_db_data` separately in your own code.

## Explanation
The `combine_data` function simply concatenates the two data sets with `pandas.concat`. This approach works when both sources share the same column names. Because the logic is split into separate functions, you can easily reuse them in other projects or extend them with additional data sources.
