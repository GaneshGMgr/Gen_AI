import os
from pathlib import Path

list_of_files = [
    ".GitHub/workflows/.gitkeep",
    "CodeSage/__init__.py",
    "CodeSage/components/data_ingestion.py",
    "CodeSage/components/data_preprocessing.py",
    "CodeSage/components/model_loading.py",
    "CodeSage/components/model_evaluation.py",
    "CodeSage/components/static_analysis.py",
    "CodeSage/components/voice_interface.py",
    "CodeSage/pipeline/inference.py",
    "CodeSage/pipeline/training.py",
    "CodeSage/logger.py",
    "CodeSage/exception.py",
    "CodeSage/config.py",
    "CodeSage/ai_integration.py",
    "CodeSage/voice_assistant.py",
    "CodeSage/static_tools.py",
    "templates/index.html",
    "statics/style.css",
    "notebook/experiment.ipynb",
    "scripts/init_setup.sh",
    "requirements.txt",
    "Dockerfile",
    "app.py",
    "setup.py",
    ".env",
    ".gitignore",
    "redis_cache.py",
    "mongodb_setup.py",
    "langchain_integration.py",
    "rasa_nlu.py",
    "prometheus_monitoring.py",
    "locust_testing.py",
    "vscode_extension/src/extension.ts",
    "vscode_extension/src/server.ts",
    "vscode_extension/package.json",
    "vscode_extension/README.md"
]


# Creating directories and files
for filepath in list_of_files:
    filepath = Path(filepath)

    filepath.parent.mkdir(parents=True, exist_ok=True)     # Create directories if they don't exist
    if not filepath.exists():
        filepath.touch()     # Create the file if it doesn't exist
        print(f"Created: {filepath}")
    else:
        print(f"Already exists: {filepath}")
