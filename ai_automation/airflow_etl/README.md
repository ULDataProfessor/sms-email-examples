# 🚀 Airflow ETL Example

This folder contains a minimal ETL pipeline using Apache Airflow. The DAG extracts
JSON from a REST API, converts the data to Parquet with pandas, and loads it into
a PostgreSQL data warehouse. Slack notifications report success or failure.

## DAG Overview
- **Schedule**: Daily at midnight (`0 0 * * *`)
- **Tasks**:
  1. `extract` – call the REST API and save the response as JSON
  2. `transform` – validate and cast the JSON then write a Parquet file
  3. `load` – load the Parquet data into PostgreSQL
  4. `notify` – send a Slack message summarizing the run

## Airflow Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create connections in the Airflow UI:
   - **postgres_default** – connection string to the data warehouse
   - **slack_default** – Slack API token
3. Define the following Airflow Variables (or env vars):
   - `API_ENDPOINT` – URL for the REST API

## Monitoring & Troubleshooting
- Use the Airflow web UI to monitor DAG runs and task logs.
- Failed tasks trigger a Slack notification detailing the error.
- Check the logs for connectivity issues (API or database) or data validation
  errors during the transform step.
