import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_FILE = Path(__file__).parent / 'pipeline.log'

# Configure root logger
logger = logging.getLogger('error_handling_logging')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Rotating file handler (daily rotation, keep 7 days)
file_handler = TimedRotatingFileHandler(LOG_FILE, when='D', interval=1, backupCount=7)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

