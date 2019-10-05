from flask import Flask, render_template, current_app
import datetime, time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config.from_pyfile("config.py")

from flask_cors import CORS
cors = CORS(app)

from server.view.message import socketio, recv_callback
socketio.init_app(app)

from server.model import db
db.init_app(app)

from server.serial_communication import device
device.init_app(app, db, port='COM6', recv_callback=recv_callback)


@app.route('/', methods=['GET'])
def index():
    return datetime.datetime.now().strftime('%M:%S')


port = 8000
if __name__ == '__main__':
    device.start_loop()
    socketio.run(app, host='127.0.0.1', debug=True, port=port, use_reloader=False)
