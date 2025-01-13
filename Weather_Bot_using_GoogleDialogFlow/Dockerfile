FROM python:3.12-slim-buster
# Set the working directory inside the container
WORKDIR /service
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy the rest of the project files into the container
COPY . ./
# entry point for the container to run the chatbot using the 'run-chatbot' command defined in setup.py
ENTRYPOINT [ "run weatherChatbot" ]
