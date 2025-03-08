from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Retrieve API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is missing. Make sure it is set in the .env file.")

openai.api_key = api_key

# Set the default model
MODEL_NAME = "gpt-4o"

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with frontend

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"response": bot_reply})

    except openai.error.RateLimitError:
        return jsonify({"error": "API quota exceeded."}), 429
    except openai.OpenAIError as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
