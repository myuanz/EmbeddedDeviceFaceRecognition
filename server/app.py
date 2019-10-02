from flask import Flask, render_template, current_app
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import datetime, time
# from flask_cors import CORS
import threading
import socketio as sockio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# cors = CORS(app)
socketio = SocketIO(app, engineio_logger=False, cors_allowed_origins='*')


@socketio.on('connect', namespace='/main')
def connect():
    emit('test', {'data': 'Connected'})
    print('Client connected')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@socketio.on('subscribeToTimer', namespace='/test')
def subscribeToTimer(interval):
    interval /= 1000

    def send_time(interval):
        # print(datetime.datetime.now())
        # socketio = current_app.extensions['socketio']
        socketio.emit('timer', {'timestamp': time.time()}, namespace='/test')
        # send('has entered the room.', room=room)
        threading.Timer(interval, send_time, [interval]).start()
    # emit('timer', [datetime.datetime.now().strftime('%M:%S')])
    send_time(interval)



@app.route('/', methods=['GET'])
def index():
    return datetime.datetime.now().strftime('%M:%S')


port = 8000
if __name__ == '__main__':

    socketio.run(app, host='127.0.0.1', debug=True, port=port)
