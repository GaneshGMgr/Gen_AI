import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import sys

# Creating logs directory to store log files
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Creating log file name based on the current timestamp
CURRENT_TIME_STAMP = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_file_name = f"log_{CURRENT_TIME_STAMP}.log"
log_file_path = LOG_DIR / log_file_name

# Setting up logging
try:
    # Creating a rotating file handler to handle large log files
    handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3)
    logging.basicConfig(
        level=logging.INFO,  # Set log level to INFO, can be changed as needed
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
        handlers=[handler]  # Adding the file handler to the logger
    )
except Exception as e:
    print(f"Error setting up logging: {e}")
    sys.exit(1)

# Test logging
# logging.info("Logging setup is complete.")
