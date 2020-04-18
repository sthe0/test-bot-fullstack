# -*- coding: utf-8 -*-
from flask import Blueprint, request
from project.bot import Bot
from project.common import app, db, fb_api
from project.models import Client


facebook = Blueprint('facebook', __name__)
bot = Bot(fb_api, db)


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
            client_id = x['sender']['id']
            bot.on_message(_get_client(client_id), incoming_text)
    db.session.commit()
    return 'ok'


def _get_client(id):
    client = db.session.query(Client).get(id)
    if client is None:
        client = Client(**fb_api.get_client_info(id))
        db.session.add(client)
    return client
