import fetch_json, bad_juju, logging
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock

"""
save a list of users that are connected
"""
connected_users = []

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
        try:
            d = fetch_json.update_conn()
            u = connected_users
            b = bad_juju.process_data('offline')
            socketio.emit('updateData', {"conn":d, "users":u, "badip":b})
            socketio.sleep(0.2)
        except Exception as ex:
            socketio.sleep(0.5)
            print(ex)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    # create_report = fetch_data.create_report()
    return render_template('report.htm')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    print(f'Client connected at {request.remote_addr}')
    if request.remote_addr not in connected_users:
        connected_users.append(request.remote_addr)
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