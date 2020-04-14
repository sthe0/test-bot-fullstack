# -*- coding: utf-8 -*-
import requests


class FacebookApi:
    FB_API_URL = 'https://graph.facebook.com/v2.6'

    def __init__(self, verify_token, page_access_token):
        self._verify_token = verify_token
        self._page_access_token = page_access_token

    @staticmethod
    def from_config(config):
        return FacebookApi(verify_token=config.VERIFY_TOKEN, page_access_token=config.PAGE_ACCESS_TOKEN)

    def verify(self, query_args):
        if query_args.get('hub.verify_token') == self._verify_token:
            return query_args.get('hub.challenge')
        else:
            return query_args

    def send_message(self, recipient_id, text):
        return requests.post(
            self.FB_API_URL + '/me/messages',
            params={
                'access_token': self._page_access_token
            },
            json={
                'messaging_type': 'RESPONSE',
                'message': {
                    'text': text
                },
                'recipient': {
                    'id': recipient_id
                },
                'notification_type': 'regular'
            }
        ).json()

    def send_tag_message(self, recipient_id, text, tag='ACCOUNT_UPDATE'):
        return requests.post(
            self.FB_API_URL + '/me/messages',
            params={
                'access_token': self._page_access_token
            },
            json={
                'messaging_type': 'MESSAGE_TAG',
                'tag': tag,
                'message': {
                    'text': text
                },
                'recipient': {
                    'id': recipient_id
                },
                'notification_type': 'regular'
            }
        ).json()

    @staticmethod
    def is_user_message(message):
        return (
            message.get('message') and
            message['message'].get('text') and
            not message['message'].get('is_echo')
        )

    def get_client_info(self, id):
        fields = [
            'name',
            'first_name',
            'last_name',
            'profile_pic',
            'locale',
            'timezone',
            'gender'
        ]
        response = requests.get(
            self.FB_API_URL + '/{id}'.format(id=id),
            params={
                'fields': ','.join(fields),
                'access_token': self._page_access_token
            }
        ).json()
        result = {field: response.get(field) for field in fields}
        result['id'] = id
        if result.get('profile_pic'):
            result['profile_pic'] = requests.get(result.get('profile_pic')).raw.read()
        return result
