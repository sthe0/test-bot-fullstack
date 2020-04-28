# -*- coding: utf-8 -*-
import json
from project.models import Message


class Bot:
    def __init__(self, fb_api, db):
        self._fb_api = fb_api
        self._db = db

    def on_message(self, client, incoming_text):
        texts = []
        for message in client.messages[:4]:
            author = 'Me'
            if message.from_client:
                author = 'You'
            texts.append('{0} [{1}]: {2}'.format(author, message.date.strftime('%d.%m.%Y %H:%M:%S'), message.text))
        client.messages.append(Message(client_id=client.id, text=incoming_text, from_client=True))
        session = self.get_session(client)
        count = session.get('count', 0)
        response_text = 'Count: {0}'.format(count)
        session['count'] = count + 1
        client.messages.append(Message(client_id=client.id, text=response_text, from_client=False))
        self.set_session(client, session)
        self._fb_api.send_message(client.id, response_text + '\n' + 'History: ' + '\n'.join(texts))

    def get_session(self, client):
        if client.session:
            return json.loads(client.session)
        return {}

    def set_session(self, client, session):
        client.session = json.dumps(session)
