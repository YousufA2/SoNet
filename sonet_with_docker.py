from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app)

# Storage for videos and chat messages
videos = []
messages = []

# Content moderation filter
def is_content_appropriate(content):
    banned_words = ["inappropriate", "banned", "badword"]
    return not any(word in content.lower() for word in banned_words)

@app.route('/')
def home():
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    description = request.form['description']

    if not is_content_appropriate(title) or not is_content_appropriate(description):
        return "Content not allowed!", 400

    videos.append({'title': title, 'description': description})
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    if not is_content_appropriate(msg):
        send("Message not allowed!", broadcast=False)
        return
    messages.append(msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
