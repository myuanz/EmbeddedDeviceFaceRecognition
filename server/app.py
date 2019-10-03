from flask import Flask, render_template, current_app
import datetime, time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config.from_pyfile("config.py")


from flask_cors import CORS
cors = CORS(app)

from view.message import socketio
socketio.init_app(app)

from model import db
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return datetime.datetime.now().strftime('%M:%S')



port = 8000
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', debug=True, port=port)
