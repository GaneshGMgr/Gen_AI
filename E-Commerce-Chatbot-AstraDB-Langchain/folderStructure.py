import os
from pathlib import Path

while True:
    project_name = input("Enter the Src folder Name: ").strip()
    if project_name != '':
        break

# List of files and directories to create
list_of_files = [
    ".GitHub/workflows/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/data_converter.py",
    f"{project_name}/ingest.py",
    f"{project_name}/retrieval_generation.py",
    "data/",
    "templates/chatbot.html",
    "statics/style.css",
    "notebook/experiment.ipynb",
    "init_setup.sh",
    "requirements.txt",
    "Dockerfile",
    "app.py",
    "logger.py",
    "exception.py",
    "setup.py",
    "MANIFEST.in",
    ".env",
    ".gitignore",
]

# Creating files and directories
for filepath in list_of_files:
    path = Path(filepath)

    if filepath.endswith("/"):  # Treat as a directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {path}")
    else:  # Treat as a file
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directories exist
        if not path.exists():
            path.touch()  # Create the file
            print(f"File created: {path}")
        else:
            print(f"File already exists: {path}")
