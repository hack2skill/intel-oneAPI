from flask import Flask, request, session
import io
from processing import *
import PyPDF2
import openai
import os
import sqlite3
from datetime import datetime
from flask_cors import CORS

SESSION = [""]
# Create the application instance and configures session
app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)


# Validates the OpenAI API key
@app.route('/key/', methods=['POST'])
def validate_key():
    try:
        key = request.json['key']
        openai.api_key = key
        model_list = openai.Model.list()  # Attempts to call the OpenAI API

        os.environ["OPENAI_API_KEY"] = key
        return {'is_valid': True}
    except:
        return {'is_valid': False}


@app.route('/signup/', methods=['POST'])
def signup():
    username = request.json["username"]
    password = request.json["password"]
    print(username, password)
    signup_valid = signup_user(username, password)
    print(signup_valid)
    if signup_valid:
        SESSION[0] = username
        return {'success': True, 'username': username}
    else:
        return {'success': False}


# Validates the user's login information
@app.route('/login/', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user_valid = validate_user(username, password)
    if user_valid:
        SESSION[0] = username
        return {'success': True, 'username': username}
    else:
        return {'success': False}


# Case where user uploads PDF
@app.route('/upload_pdf/', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return {'success': False, 'message': 'No file provided'}

        file = request.files['file']
        if file.filename == '':
            return {'success': False, 'message': 'No file selected'}

        if file.content_type != 'application/pdf':
            return {'success': False, 'message': 'Only PDF files are allowed'}

        pdf_reader = PyPDF2.PdfReader(file)
        store_text(pdf_reader, file.filename, SESSION[0])  # Passes PDF, file name (part of request object), and username

        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False, 'message': 'File uploadssss failed'}


# Case where user prompts chatbot for an answer
@app.route('/chat/', methods=['POST'])
def chat():
    try:
        query = request.json['message']
        title = request.json['title']
        response = get_reply(query, title, SESSION[0])

        return {'success': True, 'response': response}
    except Exception as e:
        print(e)
        return {'success': False, 'response': None}


@app.route('/access_messages/', methods=['POST'])
def access_messages():
    try:
        title = request.json['title']
        messages = get_chats(SESSION[0], title)

        return {'success': True, 'chat': messages}
    except:
        return {'success': False, 'chat': None}


if __name__ == "__main__":
    app.run()
