from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
import fetch_data, logging

"""
disables logging
"""
logging.getLogger("werkzeug").disabled = False

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
# Don't hard code this if you are making this public
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

"""
Grab powershell data and push to javascript
"""
def background_thread():
    print("Pulling powershell data")
    while True:
        d = fetch_data.update()
        socketio.emit('updateData', {"pshell":d})
        socketio.sleep(2)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    print(f'Client connected at {request.remote_addr}')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app, port=8080, host='0.0.0.0', debug=True)