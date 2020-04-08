import requests
import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy


FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
PAGE_ACCESS_TOKEN = 'EAAraUOWW90oBABRZAGHM6X1jWIDVSQZBt7a7C6MPCuh42zk93l0LmvtMGGO0msOPrmerlANAPt0BQUZApFiiHxZCOV0ta83sFJ8J0TchhJq04nC60WrwZAFjedZB7Smj8Vo0z9Km5BTsqwYGEl3FYKYMPfkT1f0zg97e9Q9HKo4QZDZD'
VERIFY_TOKEN = 'verify-pipe-maria-bot'


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route('/bot/facebook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return request.args


@app.route('/bot/facebook', methods=['POST'])
def handle():
    payload = request.get_json()
    event = payload['entry'][0]['messaging']
    for x in event:
        if is_user_message(x):
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond(sender_id, text)
    return 'ok'


def send_message(recipient_id, text):
    '''Send a response to Facebook'''
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


def get_bot_response(message):
    return 'echo: {}'.format(message)


def respond(sender, message):
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    return (
        message.get('message') and
        message['message'].get('text') and
        not message['message'].get('is_echo')
    )
