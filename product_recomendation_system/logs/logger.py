import logging
from pathlib import Path
from datetime import datetime
from typing import Final

# Constants
LOG_DIR: Final[Path] = Path(__file__).parent.parent / "logs"
LOG_FILE: Final[str] = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"  # ISO 8601-ish format
LOG_PATH: Final[Path] = LOG_DIR / LOG_FILE

# Configure directory (with exist_ok for thread safety)
LOG_DIR.mkdir(exist_ok=True, parents=True)

class CustomFormatter(logging.Formatter):
    """Enhanced log formatting with colors (for terminals supporting ANSI codes)"""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

# Main logger configuration
def configure_logger() -> logging.Logger:
    """Factory for configured logger instances"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # File handler (all messages)
    file_handler = logging.FileHandler(
        filename=LOG_PATH,
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler (INFO+ only)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())

    # Add handlers (avoid duplicates)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Singleton logger instance
logger: Final[logging.Logger] = configure_logger()

# Example usage
if __name__ == "__main__":
    logger.debug("Debug message (visible only in file)")
    logger.info("Info message (visible everywhere)")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical error!")