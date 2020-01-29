from flask import Flask, render_template, current_app
import datetime, time
import threading

app = Flask(__name__)
app.config.from_pyfile("config.py")

from flask_cors import CORS
cors = CORS(app)

from view.message import socketio, recv_callback
socketio.init_app(app)

from model import db
db.init_app(app)

# from server.serial_communication import device
# device.init_app(app, db, port='COM6', recv_callback=recv_callback)


@app.route('/', methods=['GET'])
def index():
    return datetime.datetime.now().strftime('%M:%S')
@app.route('/init_db', methods=['GET'])
def init_db():
    db.drop_all()
    db.create_all()
    return "ok"


port = 8000
if __name__ == '__main__':
    # device.start_loop()
    socketio.run(app, host='0.0.0.0', debug=True, port=port, use_reloader=False)
