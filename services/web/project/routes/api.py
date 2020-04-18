# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from functools import wraps
from sqlalchemy import desc

from project.common import app, db, fb_api
from project.config import ApiConfig
from project.models import Client, Message


api = Blueprint('api', __name__)


def make_error(message):
    return jsonify(error=message), 500


def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.args.get('auth_token') != ApiConfig.AUTH_TOKEN:
            return make_error('Unauthorized')
        return f(*args, **kwargs)

    return wrapper


@api.route('/bot/api/check')
@verify_token
def check():
    return 'ok'


@api.route('/bot/api/clients')
@verify_token
def clients():
    offset = int(request.args.get('start') or '0')
    limit = int(request.args.get('count') or '10')
    clients = []
    for user in db.session.query(Client).order_by(Client.id).offset(offset).limit(limit):
        clients.append(user.to_json())
    return jsonify(clients)


@api.route('/bot/api/messages/<client_id>')
@verify_token
def messages(client_id):
    if not client_id:
        return make_error('No client_id provided')
    offset = int(request.args.get('start') or '0')
    limit = int(request.args.get('count') or '10')
    messages = []
    for message in (
        db.session.query(Message)
        .filter(Message.client_id == client_id)
        .order_by(desc(Message.date))
        .offset(offset)
        .limit(limit)
    ):
        messages.append(message.to_json())
    return jsonify(messages)


@api.route('/bot/api/send/tag/<client_id>')
@verify_token
def send_tag(client_id):
    text = request.args.get('text', '')
    tag = request.args.get('tag', 'ACCOUNT_UPDATE')
    if not client_id:
        return make_error('No recipient_id provided')
    if not text:
        return make_error('No text provided')
    db.session.add(Message(client_id=client_id, text=text, from_client=False))
    db.session.commit()
    return jsonify(fb_api.send_tag_message(client_id, text, tag))


@api.route('/bot/api/send/message/<client_id>')
@verify_token
def send_message(client_id):
    text = request.args.get('text', '')
    if not client_id:
        return make_error('No recipient_id provided')
    if not text:
        return make_error('No text provided')
    db.session.add(Message(client_id=client_id, text=text, from_client=False))
    db.session.commit()
    return jsonify(fb_api.send_message(client_id, text))
