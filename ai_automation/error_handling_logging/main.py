import json
import os
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests

from .config import logger
from .process import process_records
from .utils import ValidationError, APIError, ProcessingError


def read_input(path: Path) -> List[Dict[str, str]]:
    try:
        if not path.exists():
            raise ValidationError(f"Input file {path} does not exist")
        if path.suffix.lower() == '.csv':
            df = pd.read_csv(path)
            return df.to_dict(orient='records')
        if path.suffix.lower() == '.json':
            with path.open() as f:
                return json.load(f)
        raise ValidationError('Unsupported file type')
    except Exception as exc:
        raise ValidationError(str(exc)) from exc


def save_output(path: Path, records: List[Dict[str, str]]) -> None:
    try:
        with path.open('w') as f:
            json.dump(records, f, indent=2)
    except Exception as exc:
        raise APIError(str(exc)) from exc


def send_alert(message: str) -> None:
    webhook = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook:
        return
    try:
        requests.post(webhook, json={'text': message}, timeout=5)
    except requests.RequestException as exc:
        logger.warning('Failed to send alert: %s', exc)


def main(input_path: str, output_path: str) -> None:
    logger.info('Starting pipeline')
    try:
        records = read_input(Path(input_path))
        logger.debug('Read %d records', len(records))
    except ValidationError as exc:
        logger.error('Validation error: %s', exc)
        send_alert(f'Validation error: {exc}')
        return

    try:
        processed = process_records(records)
        logger.debug('Processed %d records', len(processed))
    except ProcessingError as exc:
        logger.error('Processing error: %s', exc)
        send_alert(f'Processing error: {exc}')
        return

    try:
        save_output(Path(output_path), processed)
        logger.info('Saved output to %s', output_path)
    except APIError as exc:
        logger.error('Failed to save output: %s', exc)
        send_alert(f'Output error: {exc}')
        return

    logger.info('Pipeline completed successfully')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run error handling pipeline')
    parser.add_argument('input', help='Path to input CSV or JSON')
    parser.add_argument('-o', '--output', default='output.json', help='Output JSON path')
    args = parser.parse_args()

    main(args.input, args.output)
