# -*- coding: utf-8 -*-
import attr
import json
import logging
from project.models import Client, Message


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@attr.s
class EventInfo:
    page_id = attr.ib()
    time = attr.ib()
    sender_id = attr.ib()
    recipient_id = attr.ib()


class Bot:
    def __init__(self, fb_api, db):
        self._fb_api = fb_api
        self._db = db

    def on_entry(self, entry):
        messaging_event = entry['messaging'][0]
        if 'message' in messaging_event:
            if not self._fb_api.is_user_message(messaging_event):
                return
            raw = messaging_event['message']
            client_id = messaging_event['sender']['id']
            self.on_message(
                event_info=EventInfo(
                    page_id=entry['id'],
                    time=entry['time'],
                    sender_id=messaging_event['sender']['id'],
                    recipient_id=messaging_event['recipient']['id']
                ),
                message=Message(
                    id=raw['mid'],
                    client_id=client_id,
                    text=raw['text'],
                    from_client=True
                )
            )
            return
        logger.info('Unhandled event: ' + json.dumps(messaging_event, indent=2))

    def on_message(self, event_info, message):
        texts = []
        client = self.get_client(message.client_id)
        for message in client.messages[:4]:
            author = 'Me'
            if message.from_client:
                author = 'You'
            texts.append('{0} [{1}]: {2}'.format(author, message.date.strftime('%d.%m.%Y %H:%M:%S'), message.text))
        client.messages.append(message)
        session = self.get_session(client)
        count = session.get('count', 0)
        response_text = 'Count: {0}'.format(count)
        session['count'] = count + 1
        client.messages.append(Message(
            id=message.id + '_bot',
            client_id=client.id,
            text=response_text,
            from_client=False
        ))
        self.set_session(client, session)
        self._fb_api.send_message(client.id, response_text + '\n' + 'History: ' + '\n'.join(texts))

    @staticmethod
    def get_session(client):
        if client.session:
            return json.loads(client.session)
        return {}

    @staticmethod
    def set_session(client, session):
        client.session = json.dumps(session)

    def get_client(self, id):
        client = self._db.session.query(Client).get(id)
        if client is None:
            client = Client(**self._fb_api.get_client_info(id))
            self._db.session.add(client)
        return client
