from flask_socketio import SocketIO, emit, join_room, leave_room, send
import threading
import time
socketio = SocketIO(engineio_logger=False, cors_allowed_origins='*')

@socketio.on('connect', namespace='/test')
def connect():
    emit('test', {'data': 'Connected'})
    # print('Client connected')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    # print('Client disconnected')
    pass

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
