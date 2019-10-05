from flask_socketio import SocketIO, emit, join_room, leave_room, send
import threading
import time
from server.serial_communication import device
import json
from server.model import db, Account, FaceFeature, AssociationRecord
from typing import List

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


@socketio.on('send_message_to_device', namespace='/test')
def send_message_to_device(type: str, param: dict):
    data = device._build_json(type, param)
    device._send_message(data)

@socketio.on('create_user', namespace='/test')
def create_user(name: str, ID: str):
    assert len(ID) == 9
    account = Account.query.get(ID)
    if account is None:
        account = Account(sj_ID=ID, name=name)
    else:
        account.name = name

    db.session.add(account)
    db.session.commit()
    recv_callback({'msg': '创建用户OK'})


@socketio.on('get_users', namespace='/test')
def create_user():
    accounts: List[Account] = Account.query.all()
    ret = [
        {
            'name': account.name,
            'ID': account.sj_ID
        }
        for account in accounts
    ]
    emit('get_users', ret)

@socketio.on('create_association', namespace='/test')
def create_association(uid: str, id: str):

    assert len(id) == 9
    face_feature: FaceFeature = FaceFeature.query.get(uid)
    print(uid, id, face_feature)
    if face_feature:
        account: Account = Account.query.get(id)
        if not account:
            account: Account = Account(sj_ID=id)

        face_feature.account_sj_ID = id
        face_feature.account = account
        db.session.add(account)
        db.session.add(face_feature)
        db.session.commit()
        recv_callback({'msg': '添加关联OK'})


def recv_callback(obj: dict):
    socketio.emit('recv_callback', obj, namespace='/test')
