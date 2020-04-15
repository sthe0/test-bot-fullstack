# -*- coding: utf-8 -*-
import os

from flask import (
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
    login_required
)

from .common import app, db, fb_api
from .models import Client, Message, User, Role


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_datastore.create_user(email='admin@fedor-solovyev.ru', password='P@ssw0rd@')
    db.session.commit()


@app.route('/test')
def test():
    return jsonify(hello='test')


@app.route('/')
def home():
    return jsonify(hello='home')


@app.route('/other')
@login_required
def other():
    return jsonify(hello='other')


# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)


@app.route('/bot/facebook', methods=['GET'])
def verify():
    return fb_api.verify(request.args)


@app.route('/bot/facebook', methods=['POST'])
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
