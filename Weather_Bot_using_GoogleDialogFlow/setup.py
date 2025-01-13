from setuptools import setup, find_packages

REQUIREMENT_FILE_NAME = "requirements.txt"
REMOVE_PACKAGE = "-e ."

def get_requirement_list(requirement_file_name=REQUIREMENT_FILE_NAME) -> list:
    try:
        # Read the requirements.txt file and process it
        requirement_list = []
        with open(requirement_file_name) as requirement_file:
            # Process each line and remove unwanted entries
            requirement_list = [requirement.strip() for requirement in requirement_file.readlines()]
            if REMOVE_PACKAGE in requirement_list:
                requirement_list.remove(REMOVE_PACKAGE)
        return requirement_list
    except Exception as e:
        print(f"Error reading {requirement_file_name}: {e}")
        raise

setup(
    name="google_dialogflow_chatbot",
    version="0.0.1",
    author="google_dialogflow-Chatbot",
    author_email="googledialogflowChatbot@gmail.com",
    description="Chatbot using Google Dialogflow",
    long_description="A simple chatbot using Google Dialogflow for weather queries.",
    long_description_content_type="text/markdown",  # Optional, if using markdown for long description
    license="MIT",
    packages=find_packages(),  # Automatically finds and includes packages
    install_requires=get_requirement_list(),
    include_package_data=True,  # Ensures non-Python files (e.g., templates, static files) are included
    entry_points={  
        'console_scripts': [
            'weatherChatbot=app:main',  # Entry point to the chatbot script (directly from app.py)
        ],
    },
)

# pip install -e .
# python setup.py install