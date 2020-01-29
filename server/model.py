from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Account(db.Model):
    sj_ID = db.Column(db.String(9), primary_key=True)  # student and job ID 学工号
    name = db.Column(db.String(12))
    is_admin = db.Column(db.Boolean)
    note = db.Column(db.Text)


class FaceFeature(db.Model):
    UID = db.Column(db.String(32), primary_key=True)
    account = db.relationship(
        "Account",
        backref=db.backref('face_features', lazy='dynamic'),
    )
    account_sj_ID = db.Column(db.String(9), db.ForeignKey('account.sj_ID'))
    feature = db.Column(db.BLOB(1024))
    img_path = db.Column(db.String(64))



class AssociationRecord(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    operator_account_sj_ID = db.Column(db.String(9), db.ForeignKey('account.sj_ID'))

    operator_account = db.relationship(
        "Account",
        backref=db.backref('association_record', lazy='dynamic'),
    )

    create_time = db.Column(db.DateTime)

    face_feature = db.relationship(
        "FaceFeature",
        backref=db.backref('association_record', lazy='dynamic'),
    )
    face_feature_UID = db.Column(db.String(32), db.ForeignKey('face_feature.UID'))


    def __init__(self, **kwargs):
        self.create_time = datetime.now()
        super().__init__(**kwargs)


class RecognitionRecord(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    face_feature = db.relationship(
        "FaceFeature",
        backref=db.backref('recognition_record', lazy='dynamic'),
    )
    face_feature_UID = db.Column(db.String(32), db.ForeignKey('face_feature.UID'))

    def __init__(self, **kwargs):
        self.create_time = datetime.now()
        super().__init__(**kwargs)
