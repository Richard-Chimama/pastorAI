import ollama
from flask import Flask, jsonify, request

MODEL = "pastor-ai"
app = Flask(__name__)

def generateResponse(text):
    response = ollama.chat(model=MODEL, messages=[{
    "role": "user", 
    "content": f"{text}"
    }])

    return response['message']['content']



@app.route('/message', methods=['POST'])
def process_message():
    message = request.get_json()['message']
    

    try:
        if message is not None:
            response = generateResponse(str(message))
        else:
            response = {'response': 'Error from the text: ' + str(message)}
    except EOFError:
        print("failed to retrive the response")


    
    # You can add your own logic here
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)