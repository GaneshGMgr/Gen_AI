from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from E_commChatbot.retrieval_generation import generation
from E_commChatbot.ingest import ingestdata
from logger import logging

app = Flask(__name__)

load_dotenv()

vstore=ingestdata("done")
chain=generation(vstore)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]  # Get message from the form
    input = msg
    result = chain.invoke(input)

    logging.info(f"User message: {msg}")
    logging.info(f"Response from chain: {result}")
    
    return result  

if __name__ == '__main__':
    app.run(debug=True)
