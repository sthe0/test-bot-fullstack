# -*- coding: utf-8 -*-
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy.ext.declarative import declarative_base
from .common import db


# Base = declarative_base()
db.Model.query = db.session.query_property()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))


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
