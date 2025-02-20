import os
import ollama
from flask import Flask, jsonify, request
from uuid import uuid4
from datetime import datetime

# Constants
MODEL = "pastor-ai"
app = Flask(__name__)

PORT = int(os.getenv("PORT", 8000))

# In-memory storage for chat history
chat_history = {}

def generate_daily_devotion():
    """Generate a daily devotion with a Bible verse and reflection."""
    today = datetime.today().strftime("%B %d, %Y")  # Example: "February 16, 2025"

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a pastor writing a short daily devotion based on the Bible."},
            {"role": "user", "content": f"Write a short, inspiring daily devotion for {today} with a Bible verse and reflection."}
        ]
    )

    return response["message"]["content"]

def generate_sermon():
    """Generate a sermon based on the Bible, addressing modern or end-time themes."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a wise apostle of Jesus Christ. Write a sermon based on the Bible, rebuking sin where necessary and aligning it with modern or end-time church age."},
            {"role": "user", "content": "Write a sermon that addresses sin and aligns with modern or end-time church age."}
        ]
    )
    return response['message']['content']

def generate_response(messages):
    """Generate a response based on the provided chat history."""
    response = ollama.chat(model=MODEL, messages=messages)
    return response['message']['content']

@app.route('/chat', methods=['POST'])
def process_message():
    """Process a user message and return a response."""
    data = request.get_json()
    message = data.get('message')
    user_id = data.get('user_id')

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    try:
        if user_id not in chat_history:
            chat_history[user_id] = []

        chat_history[user_id].append({"role": "user", "content": message})
        response = generate_response(messages=chat_history[user_id])
        chat_history[user_id].append({"role": "assistant", "content": response})

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Failed to process message: {str(e)}"}), 500

@app.route('/new-user', methods=['GET'])
def create_new_user():
    """Generate a new user ID."""
    user_id = str(uuid4())
    return jsonify({"user_id": user_id})

@app.route('/user-chat', methods=['POST'])
def get_user_chat():
    """Retrieve chat history for a specific user."""
    user_id = request.get_json().get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    messages = chat_history.get(user_id, [])
    return jsonify(messages)

@app.route('/sermon', methods=['GET'])
def get_sermon():
    """Generate and return a sermon."""
    try:
        sermon = generate_sermon()
        return jsonify({"sermon": sermon})
    except Exception as e:
        return jsonify({"error": f"Failed to generate sermon: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)