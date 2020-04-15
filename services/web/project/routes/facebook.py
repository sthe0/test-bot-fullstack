# -*- coding: utf-8 -*-
from flask import Blueprint, request
from project.common import app, db, fb_api
from project.models import Client, Message


facebook = Blueprint('facebook', __name__)


@facebook.route('/bot/facebook', methods=['GET'])
def verify():
    return fb_api.verify(request.args)


@facebook.route('/bot/facebook', methods=['POST'])
def handle():
    payload = request.get_json()
    event = payload['entry'][0]['messaging']
    for x in event:
        if fb_api.is_user_message(x):
            incoming_text = x['message']['text']
            sender_id = x['sender']['id']

            client = get_client(sender_id)
            response_text = process_message(client, incoming_text)
            fb_api.send_message(sender_id, response_text)
    db.session.commit()
    return 'ok'


def process_message(client, incoming_text):
    texts = []
    for message in client.messages[:4]:
        author = 'Me'
        if message.from_client:
            author = 'You'
        texts.append('{0} [{1}]: {2}'.format(author, message.date.strftime('%d.%m.%Y %H:%M:%S'), message.text))
    client.messages.append(Message(client_id=client.id, text=incoming_text, from_client=True))
    response_text = 'Buy an elephant!'
    client.messages.append(Message(client_id=client.id, text=response_text, from_client=False))
    return response_text + '\n' + 'History: ' + '\n'.join(texts)


def get_client(id):
    client = db.session.query(Client).get(id)
    if client is None:
        client = Client(**fb_api.get_client_info(id))
        db.session.add(client)
    return client
