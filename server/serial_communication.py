import threading
import serial
from model import Account, FaceFeature, AssociationRecord, RecognitionRecord, db
from time import sleep, time
import json
import socket
import random
import string


class Device:
    port = ''
    baudrate = 0
    IP = ''

    s: serial.Serial = None
    message = []
    recv_callback = lambda x, y: (x, y)
    db = None
    app = None

    def __init__(self, port, baudrate=115200, IP=None):
        self.port = port
        self.baudrate = baudrate

    def init_app(self, app, db, port=None, baudrate=None, recv_callback=None):
        self.app = app
        self.db = db
        self.recv_callback = recv_callback

        if port:
            self.port = port
        if baudrate:
            self.baudrate = baudrate

    def start_loop(self):
        while True:
            try:
                self.s = serial.Serial(self.port, self.baudrate)
                break
            except Exception as e:
                print(e)
        thr = threading.Thread(target=self._loop)
        thr.start()
        return self.s.is_open

    def _loop(self):
        while True:

            obj = self._recv_message()
            self.recv_callback(obj)
            # self.message.append(obj)
            msg_type = obj.get('type')
            if msg_type == 'face_info':
                if obj.get("msg") == 'have face':
                    print(obj['info'].get("score"))
                    if obj['info'].get("score") > 90:
                        if self.db:
                            with self.app.app_context():
                                face_feature: FaceFeature = FaceFeature.query.get(obj['info'].get('uid'))
                                if face_feature:
                                    record: RecognitionRecord = RecognitionRecord(face_feature=face_feature)

                                    if face_feature.account is not None:
                                        self.recv_callback(f"为{face_feature.account.name}开门")
                                        s = socket.socket()
                                        s.connect(('10.18.52.130', 8080))
                                        s.send(b'b1e')
                                        s.close()
                                    self.db.session.add(record)
                                    self.db.session.commit()
                                else:
                                    face_feature: FaceFeature = FaceFeature(UID=obj['info'].get('uid'),
                                                                            feature=obj['info'].get("feature"))
                                    self.db.session.add(face_feature)
                                    self.db.session.commit()
                    elif obj['info'].get("score") <= 60:
                        if obj['info'].get('feature') == 'null':
                            # 未知的脸
                            self._set_cfg(auto_out_feature=1, out_feature=1)  # 设置为不识别只获取
                            # print("_set_cfg 1")
                            pass
                        else:
                            if self.db:
                                uid = hex(int(time() * 0xf))[2:].upper()
                                uid = uid + "".join(
                                    random.sample(string.ascii_uppercase + string.digits, 32 - len(uid))
                                )  # 防止2038问题
                                with self.app.app_context():
                                    face_feature: FaceFeature = self.save_feature(uid, obj['info'].get('feature'),
                                                                                  commit=False)
                                    record: RecognitionRecord = RecognitionRecord(face_feature=face_feature)
                                    self.db.session.add(record)
                                    self.db.session.commit()
                            self._set_cfg(auto_out_feature=2, out_feature=1)  # 设置为识别
                            # print("_set_cfg 0")
            # 2^31 = 2*2^30 = 2*4^15 = 0.5 * 4^16 = 0.5 * 16^4
            print(obj)

    @staticmethod
    def _build_json(type: str, param: dict, version=1, encoding='utf-8') -> bytes:
        data = {
            'version': version,
            'type': type,
        }
        data.update(param)
        data = json.dumps(data) + "\r\n"
        return data.encode(encoding)

    @staticmethod
    def _parse_result(data: bytes, encoding='utf-8') -> dict:
        return json.loads(data, encoding=encoding)

    def _send_message(self, data: bytes) -> None:
        assert data.endswith(b'\r\n')
        assert data.count(b'\r\n') == 1

        while not self.s.writable():
            pass
        self.s.write(data)
        print('send', data)

    def _recv_message(self) -> dict:
        data = b''
        while True:
            data += self.s.read_all()
            if not data.endswith(b'\r\n'):
                sleep(0.02)
                continue
            else:
                obj = self._parse_result(data)
                return obj

    def save_feature(self, UID: str, feature: str, account_sj_ID=None, commit=True) -> FaceFeature:
        assert len(feature) == 264
        assert len(UID) == 32
        print('save_feature')
        face_feature = FaceFeature(UID=UID, feature=feature, account_sj_ID=account_sj_ID)
        self.db.session.add(face_feature)
        self._add_uer_by_fea(face_feature.UID, face_feature.feature)
        self._recv_message()
        if commit:
            self.db.session.commit()
        return face_feature

    def _add_uer_by_fea(self, UID: str, feature: str):
        data = self._build_json(
            'add_uer_by_fea',
            {'user': {
                'uid': UID,
                'fea': feature
            }}
        )
        self._send_message(data)

    def _set_cfg(
            self,
            uart_baud=115200,
            out_feature=0,
            open_delay=1,
            pkt_fix=0,
            auto_out_feature=0,
            out_interval_in_ms=500,
            fea_gate=70,
    ):
        data = self._build_json(
            'set_cfg',
            {'cfg': {
                'uart_baud': uart_baud,
                'out_feature': out_feature,
                'open_delay': open_delay,
                'pkt_fix': pkt_fix,
                'auto_out_feature': auto_out_feature,
                'out_interval_in_ms': out_interval_in_ms,
                'fea_gate': fea_gate,
            }}
        )
        self._send_message(data)

        def __del__(self):
            self.s.close()


device = Device('COM6', 115200)

if __name__ == "__main__":
    device = Device('COM6', 115200)
    device.start_loop()
