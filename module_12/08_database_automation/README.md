# Database Automation

## Project Overview
`upsert_data.py` loads a CSV file into a PostgreSQL table. Existing rows are updated and new rows inserted so the target table stays in sync with the file contents.

## Variables
`CSV_PATH` defines the input file, while the database connection uses environment variables such as `PGHOST` and `PGDATABASE`. The SQL statement references the table `public.data_table` but you may change it inside the script.

## Instructions
Install dependencies with `pip install pandas psycopg2-binary`. Ensure your database is accessible and that connection environment variables are set. Then run `python upsert_data.py` to process the CSV in batches of 100 rows.

## Explanation
The script opens a connection with `psycopg2` and uses `execute_batch` to perform an UPSERT using PostgreSQL's `ON CONFLICT` clause. Batching the inserts reduces transaction overhead when handling large files.
