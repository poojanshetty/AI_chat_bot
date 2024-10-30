from flask import Flask, render_template, request, jsonify
from Ai_chat_bot import chat, handle_query
import os

app = Flask(__name__)

@app.route('/')
def index():
    a = os.getcwd()
    print(f"Current Directory: {a}")
    return render_template('templates/index.html')

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.form['message']
    response = chat(user_message)
    return jsonify({'response': response})

@app.route('/command', methods=['POST'])
def execute_command():
    user_command = request.form['command']
    handle_query(user_command)
    return jsonify({'status': 'Executed'})


if __name__ == '__main__':
    app.run(debug=True)
