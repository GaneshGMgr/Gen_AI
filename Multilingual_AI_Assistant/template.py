import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "research/notebook.ipynb",
    "src/__init__.py",
    "src/helper.py",
    ".gitignore"
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
]


for filepath in list_of_files:
    filepath = Path(filepath) # Convert to a Path object
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True) # Create directories if needed
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

     # Create the file if it doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")