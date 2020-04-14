# -*- coding: utf-8 -*-
from datetime import datetime
from .common import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    profile_pic = db.Column(db.LargeBinary())
    locale = db.Column(db.String(8))
    timezone = db.Column(db.Integer())
    gender = db.Column(db.String(32))
    messages = db.relationship('Message', back_populates='client', order_by="desc(Message.date)")

    def __init__(
        self,
        id,
        name=None,
        first_name=None,
        last_name=None,
        profile_pic=None,
        locale=None,
        timezone=None,
        gender=None
    ):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.locale = locale
        self.timezone = timezone
        self.gender = gender


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(128), db.Sequence('message_id_seq'), primary_key=True)
    text = db.Column(db.String(1000))
    from_client = db.Column(db.Boolean())
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    client_id = db.Column(db.String(256), db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='messages')

    def __init__(
        self,
        client_id,
        text,
        from_client,
        date=None
    ):
        self.client_id = client_id
        self.text = text
        self.from_client = from_client
        if date is not None:
            self.date = date
