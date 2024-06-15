from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
import zmq
import threading
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for Flask-SocketIO

# ZeroMQ context
context = zmq.Context()
DELIMITER = "::"

def zmq_listener():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:7500")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv_string()
        try:
            topic, data_str = message.split(DELIMITER, 1)  # Split topic and data using delimiter
            data = json.loads(data_str)
            if topic == 'scraper_status':
                socketio.emit('scraper_status', data)
            elif topic == 'profiles_status':
                socketio.emit('profiles_status', data)
        except ValueError as e:
            print(f"Failed to split message: {e}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    send('Connected to WebSocket')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    zmq_thread = threading.Thread(target=zmq_listener)
    zmq_thread.daemon = True
    zmq_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
