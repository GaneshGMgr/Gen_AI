import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

LOGFILEPATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    level=logging.INFO, 
    filename=LOGFILEPATH, 
    format="[%(asctime)s]%(lineno)d %(name)s - %(levelname)s -%(message)s"
)

# logging.info("This is a test log message")
