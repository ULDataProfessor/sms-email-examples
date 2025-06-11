"""Simple Airflow ETL example."""
from __future__ import annotations

import json
import logging
import urllib.request
from datetime import datetime

import pandas as pd
import sqlalchemy
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from slack_sdk import WebClient


def send_slack_message(message: str) -> None:
    """Send a message to Slack using the token stored in Airflow Variables."""
    token = Variable.get("SLACK_TOKEN")
    channel = Variable.get("SLACK_CHANNEL", "#general")
    try:
        WebClient(token=token).chat_postMessage(channel=channel, text=message)
    except Exception as exc:  # pragma: no cover - notification failures shouldn't break the DAG
        logging.error("Failed to send Slack message: %s", exc)


def extract(**context) -> str:
    endpoint = Variable.get("API_ENDPOINT")
    logging.info("Requesting data from %s", endpoint)
    with urllib.request.urlopen(endpoint) as response:
        data = json.loads(response.read())
    path = "/tmp/api_data.json"
    with open(path, "w") as f:
        json.dump(data, f)
    return path


def transform(ti) -> str:
    json_path = ti.xcom_pull(task_ids="extract")
    with open(json_path) as f:
        records = json.load(f)
    df = pd.json_normalize(records)
    # Cast numeric columns to floats for simplicity
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
    parquet_path = "/tmp/api_data.parquet"
    df.to_parquet(parquet_path, index=False)
    return parquet_path


def load(ti) -> None:
    parquet_path = ti.xcom_pull(task_ids="transform")
    df = pd.read_parquet(parquet_path)
    engine = sqlalchemy.create_engine(Variable.get("POSTGRES_URI"))
    df.to_sql("api_data", engine, if_exists="append", index=False)
    engine.dispose()


def notify_success(context):
    send_slack_message(f"DAG {context['dag'].dag_id} succeeded")


def notify_failure(context):
    send_slack_message(f"DAG {context['dag'].dag_id} failed: {context['exception']}")


with DAG(
    dag_id="example_etl_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 0 * * *",
    catchup=False,
    on_failure_callback=notify_failure,
    on_success_callback=notify_success,
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task
