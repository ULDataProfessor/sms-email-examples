# Error Handling and Logging Pipeline

This example demonstrates a small data‑processing pipeline with robust error handling and logging. It reads input records from a CSV or JSON file, processes them, and saves the results. The package also supports optional Slack alerts on failures.

## Logging configuration

Logging is configured in `config.py`. A logger named `error_handling_logging` writes to both the console and a `TimedRotatingFileHandler` that rotates daily and keeps seven backups. Log messages include a timestamp, level, module name, and message.

To change log levels or handlers, modify the configuration in `config.py`. The log file location is defined by `LOG_FILE` next to the module.

## Custom exceptions

`utils.py` defines a small hierarchy:

- `PipelineError` – base class
- `ValidationError` – raised when input fails validation or is missing
- `APIError` – raised when saving output or calling external services fails
- `ProcessingError` – raised inside `process.py` when a record cannot be processed

These exceptions are caught in `main.py` and logged appropriately.

## Running the pipeline

Install requirements listed in `requirements.txt` and run:

```bash
python main.py path/to/input.csv -o output.json
```

Logs appear in the console and in `pipeline.log`. To enable Slack alerts on errors, set the environment variable `SLACK_WEBHOOK_URL` to a valid webhook URL.
