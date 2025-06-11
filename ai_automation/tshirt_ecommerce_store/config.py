"""Configuration and logging setup for T-shirt store."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / 'store.log'

# Load environment variables
ENV_PATH = os.getenv('ENV_PATH', BASE_DIR / '.env')
if isinstance(ENV_PATH, Path):
    ENV_PATH = str(ENV_PATH)
load_dotenv(ENV_PATH)

logger = logging.getLogger('tshirt_store')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
