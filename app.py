from flask import Flask, request, jsonify, session
import openai
import os
import json
import time
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is missing. Set it in the .env file.")

openai.api_key = api_key

# Flask App
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session memory
CORS(app)

# Load Knowledge Base (FAQs)
with open("knowledge_base.json", "r") as file:
    knowledge_base = json.load(file)

# Simple Cache
cache = {}

# API Authentication Token
API_SECRET_KEY = "your_super_secret_key"

@app.route('/chat', methods=['POST'])
def chat():
    # API Authentication
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_SECRET_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_message = data.get("message", "")

    # Check Cache for Previous Responses
    if user_message in cache:
        return jsonify({"response": cache[user_message]})

    # Check Knowledge Base First
    if user_message in knowledge_base:
        response_text = knowledge_base[user_message]
    else:
        # Store conversation history in session
        if "chat_history" not in session:
            session["chat_history"] = []
        session["chat_history"].append({"role": "user", "content": user_message})

        # OpenAI API Call
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=session["chat_history"]
        )

        response_text = response.choices[0].message.content
        session["chat_history"].append({"role": "assistant", "content": response_text})

    # Store response in cache for 5 minutes
    cache[user_message] = response_text
    time.sleep(5 * 60)

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
