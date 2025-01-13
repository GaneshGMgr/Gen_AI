import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(exist_ok=True)

CURRENT_TIME_STAMP = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_file_name = f"log_{CURRENT_TIME_STAMP}.log"
log_file_path = LOG_DIR / log_file_name

try:
    # Logger instance
    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.INFO)  # Set log level to INFO, can be adjusted as needed

    # Check if handlers are already added
    if not logger.hasHandlers():
        # File handler with rotating logs
        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # Console handler for debugging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

except Exception as e:
    print(f"Error setting up logging: {e}")
    raise

# # Test logging
# logger.info("Logging setup is complete.")
