import ollama
from flask import Flask, jsonify, request
from uuid import uuid4
from datetime import datetime


MODEL = "pastor-ai"
app = Flask(__name__)

chat_history = {}

def generate_daily_devotion():
    today = datetime.today().strftime("%B %d, %Y")  # Example: "February 16, 2025"

    response = ollama.chat(model=MODEL, messages=[
        {"role": "system", "content": "You are a pastor writing a short daily devotion based on the Bible."},
        {"role": "user", "content": f"Write a short, inspiring daily devotion for {today} with a Bible verse and reflection."}
    ])

    return response["message"]["content"]


def generate_sermon():
    response = ollama.chat(model=MODEL, messages=[
        {"role": "system", "content":"You are a wiser apostle of Jesus Christ, write a sermon based on the bible"},
        {"role":"user", "content": "write a sermon, rebuke sin where necessary, align the sermon if possible with modern or endtime church age."}
    ])
    return response['message']['content']

def generateResponse(messages):
    response = ollama.chat(model=MODEL, messages=messages)

    return response['message']['content']



@app.route('/chat', methods=['POST'])
def process_message():
    message = request.get_json()['message']
    user_id = request.get_json()['user_id']
    
    try:
        if user_id not in chat_history:
            chat_history[user_id] = []

        if message is not None:
            chat_history[user_id].append({"role":"user", "content": message})
            response = generateResponse(messages= chat_history[user_id])
            chat_history[user_id].append({"role":"assistant", "content": response})
        else:
            response = {'response': 'Error from the text: ' + str(message)}
    except EOFError:
        print("failed to retrive the response")


        
    return jsonify(response)

@app.route('/new-user', methods=['GET'])
def create_new_user():
    user_id=str(uuid4())
    return {"user_id": user_id}

@app.route('/user-chat', methods=['POST'])
def get_user_chat():
    user_id = request.get_json()['user_id']
    try:
        messages = chat_history[user_id]
    except:
        messages = {}    
    return messages


@app.route('/sermon', methods=['GET'])
def generateSermon():
    return generate_sermon()

if __name__ == '__main__':
    app.run(debug=True)