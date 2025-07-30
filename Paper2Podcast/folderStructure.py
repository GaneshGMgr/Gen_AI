import os
import venv
import subprocess
from pathlib import Path
import platform

# Create virtual environment
venv_dir = "venv"
builder = venv.EnvBuilder(with_pip=True)
builder.create(venv_dir)
print(f"\n✅ Virtual environment created at: {os.path.abspath(venv_dir)}")

# Activation instructions
print("\n🔧 To activate the virtual environment, run:")
if platform.system() == "Windows":
    print("    .\\venv\\Scripts\\activate")
else:
    print("    source venv/bin/activate")

# File and folder structure
list_of_files = [
    ".GitHub/workflows/.gitkeep",
    "backend/agent/__init__.py",
    "backend/agent/agentic_pipeline.py",
    "backend/config/__init__.py",
    "backend/config/config.yaml",
    "backend/prompt_library/__init__.py",
    "backend/prompt_library/prompt.py",
    "backend/tools/__init__.py",
    "backend/utils/__init__.py",
    "backend/logger/__init__.py",
    "backend/logger/logger.py",
    "backend/exception/__init__.py",
    "backend/exception/exception.py",
    "backend/experiments/notebook.ipynb",
    "backend/save_documents/",
    "backend/data/",
    "backend/data/outputs/",
    "frontend/templates/index.html",
    "frontend/statics/style.css",
    "frontend/statics/media/",

    ".env",
    ".gitignore",
    "README.md",
    "init_setup.sh",
    "requirements.lock.txt",
    "setup.py",
    "app.py",
]



print("\n Creating project structure...")
for filepath in list_of_files:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Skip folder creation for trailing slashes
    if filepath.endswith("/"):
        continue

    if not path.exists():
        path.touch()
        print(f"  Created: {path}")
    else:
        print(f"  Already exists: {path}")

# Write boilerplate content to certain files
boilerplate = {
    "README.md": "# Project Title\n\nDescribe your project here.\n",
    ".gitignore": "venv/\n__pycache__/\n.env\n*.pyc\n",
    "app.py": 'print("Hello, world! Your app is ready.")\n',
}

for filename, content in boilerplate.items():
    file_path = Path(filename)
    if file_path.exists() and file_path.stat().st_size == 0:
        file_path.write_text(content)
        print(f"  Wrote boilerplate to: {filename}")

# Install requirements if file exists
requirements_file = Path("requirements.lock.txt")
if requirements_file.exists() and requirements_file.stat().st_size > 0:
    print("\n Installing dependencies from requirements.lock.txt...")
    pip_executable = (
        "venv\\Scripts\\pip.exe" if platform.system() == "Windows" else "venv/bin/pip"
    )
    subprocess.run([pip_executable, "install", "-r", str(requirements_file)])
    print(" Dependencies installed.")
else:
    print("\n  No requirements.lock.txt found or it's empty — skipping install.")

print("\n Setup complete!")
