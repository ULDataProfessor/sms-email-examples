"""Configuration loader for the car insurance rating service."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from a .env file located next to this module
ENV_PATH = Path(__file__).resolve().parent / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

BASE_RATE = float(os.getenv('BASE_RATE', '500'))
VIN_API_KEY = os.getenv('VIN_API_KEY', '')
RECORD_API_KEY = os.getenv('RECORD_API_KEY', '')
LOCATION_API_KEY = os.getenv('LOCATION_API_KEY', '')

# Optional base URLs for the external services
VIN_API_URL = os.getenv('VIN_API_URL', 'https://example.com/vin')
RECORD_API_URL = os.getenv('RECORD_API_URL', 'https://example.com/record')
LOCATION_API_URL = os.getenv('LOCATION_API_URL', 'https://example.com/location')

LOG_FILE = Path(__file__).resolve().parent / 'car_insurance.log'
