from setuptools import find_packages, setup

setup(
    name="QASystem_with_Haystack",
    version="0.0.1",
    author="QASystem",
    author_email="qasystem@gmail.com",
    packages=find_packages(include=["QASystem", "QASystem.*"]),  # Include all subpackages of QASystem
    install_requires=[
        "pinecone-haystack",
        "haystack-ai",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pathlib",
    ],
    include_package_data=True,  # Ensures non-Python files like templates are included
    package_data={
        "": ["Templates/*.html"],
    },
    entry_points={
        'console_scripts': [
            'qasystem=app:main',  # assumes app.py has a main function
        ],
    },
)

# python setup.py install