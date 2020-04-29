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
    session = db.Column(db.Text())
    messages = db.relationship('Message', back_populates='client', order_by="desc(Message.date)")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # 'profile_pic': self.profile_pic,
            'locale': self.locale,
            'timezone': self.timezone,
            'gender': self.gender
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(128), primary_key=True)
    text = db.Column(db.String(1000))
    from_client = db.Column(db.Boolean())
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    client_id = db.Column(db.String(256), db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='messages')

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'from_client': self.from_client,
            'date': self.date.isoformat()
        }
