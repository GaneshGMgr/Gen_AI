import os
from pathlib import Path

# while True:
#     project_name = input("Enter the Src folder Name: ").strip()
#     if project_name != '':
#         break

# List of files and directories to create
list_of_files = [
    ".GitHub/workflows/.gitkeep",
    ".GitHub/workflows/main.yaml",
    "app_exception/__init__.py",
    "app_exception/exception.py",
    "app_logger/__init__.py",
    "app_logger/logger.py",
    "google_dialogflow_chatbot.egg-info/",
    "notebook/experiment.ipynb",
    "templates/weatherChatbot.html",
    "statics/style.css",
    "init_setup.sh",
    "requirements.txt",
    "Dockerfile",
    "app.py",
    "weather_data.py",
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
