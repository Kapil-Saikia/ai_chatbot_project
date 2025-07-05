from flask import Flask, request, jsonify, render_template
from chatbot import get_response
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please say something!"})
    
    bot_reply = get_response(user_input)

    # Save to database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)",
        (user_input, bot_reply)
    )
    conn.commit()
    conn.close()

    return jsonify({"response": bot_reply})

# ✅ Move this ABOVE app.run
@app.route('/logs')
def show_logs():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat_logs ORDER BY id DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("logs.html", logs=logs)

# ✅ Keep app.run at the very end
if __name__ == '__main__':
    app.run(debug=True)
