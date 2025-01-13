from setuptools import find_packages, setup

setup(
    name="genaiAIProject",
    version="0.0.0",
    author="GenAI Project",
    author_email="genaiproject@gmail.com",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "pipwin",
        "pyaudio",
        "gTTS",
        "google-generativeai",
        "python-dotenv",
        "streamlit",
    ],
)


# python setup.py install