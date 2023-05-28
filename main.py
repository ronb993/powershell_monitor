import run_powershell, bad_juju, logging, os
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
logging.getLogger("werkzeug").disabled = True

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
# Don't hard code this if you are making this public
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

# prepare folders for data
def setup_files():
    if not os.path.exists('C:\\temp\\results'):
        os.makedirs('C:\\temp\\results\\bad_tcp')
        os.makedirs('C:\\temp\\results\\bad_udp')

"""
Grab powershell data and push to javascript
"""
def background_thread():
    print("Pulling powershell data")
    while True:
        try:
            tcp = run_powershell.update_tcp()
            online_users = connected_users
            bad_connections = bad_juju.process_data('offline', tcp)
            socketio.emit('updateData', {"tcp":tcp, "online_users":online_users,
                                         "bad_connections":bad_connections})
            socketio.sleep(0.2)
        except Exception as ex:
            socketio.sleep(1)
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
    setup_files()
    socketio.run(app, port=8080, host='0.0.0.0', debug=False)