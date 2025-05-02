import logging
import os
from datetime import datetime, timedelta

# Define the maximum log size (in bytes) - 2MB
MAX_LOG_SIZE = 2 * 1024 * 1024  # 2 MB

def configure_logging():
    logger = logging.getLogger('json_logger')
    logger.setLevel(logging.INFO)

    # Ensure logs directory exists
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Create a log file with the current date
    log_file = os.path.join(logs_dir, f"newrelic_data_{datetime.now().strftime('%Y-%m-%d')}.log")

    # Check if the log file exists and its size
    if os.path.exists(log_file) and os.path.getsize(log_file) >= MAX_LOG_SIZE:
        # If the log file is too big, generate a new file name
        log_file = os.path.join(logs_dir, f"newrelic_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def remove_old_logs(logs_dir):
    # Get the current date and time
    now = datetime.now()

    # Iterate over all files in the logs directory
    for filename in os.listdir(logs_dir):
        file_path = os.path.join(logs_dir, filename)

        # Check if the file is a log file
        if os.path.isfile(file_path) and filename.endswith('.log'):
            # Get the file's last modification time
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

            # Calculate the difference between now and the file's modification time
            file_age = now - file_mtime

            # If the file is older than 14 days, delete it
            if file_age > timedelta(days=14):
                os.remove(file_path)
                print(f"Deleted old log file: {file_path}")
