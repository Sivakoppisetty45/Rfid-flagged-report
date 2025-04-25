import logging
import os
from datetime import datetime


def configure_logging():
    logger = logging.getLogger('json_logger')
    logger.setLevel(logging.INFO)

    # Ensure logs directory exists
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Create a log file with current date
    log_file = os.path.join(logs_dir, f"newrelic_data_{datetime.now().strftime('%Y-%m-%d')}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger