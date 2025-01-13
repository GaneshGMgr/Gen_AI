from setuptools import find_packages, setup

setup(
    name="E-commChatbot",
    version="0.0.1",
    author="E-Chatbot",
    author_email="chatbot@gmail.com",
    packages=find_packages(include=["E-commChatbot", "E-commChatbot.*"]),
    install_requires=[
        "langchain-astradb",
        "langchain",
        "langchain-openai",
        "datasets",
        "pypdf",
        "python-dotenv",
        "flask",
        "setuptools",
    ],
    include_package_data=True,  # Ensures non-Python files are included
    package_data={  # Include specific file types from the package
        "": ["templates/*.html", "statics/*.css"],
    },
    entry_points={  # Command-line tool setup
        'console_scripts': [
            'E-commChatbot=app:main',  # Ensure app.py has a main() function
        ],
    },
)