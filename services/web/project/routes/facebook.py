# -*- coding: utf-8 -*-
from flask import Blueprint, request
from project.bot import Bot
from project.common import app, db, fb_api


facebook = Blueprint('facebook', __name__)
bot = Bot(fb_api, db)


@facebook.route('/bot/facebook', methods=['GET'])
def verify():
    return fb_api.verify(request.args)


@facebook.route('/bot/facebook', methods=['POST'])
def handle():
    payload = request.get_json()
    bot.on_entry(payload['entry'][0])
    db.session.commit()
    return 'ok'
