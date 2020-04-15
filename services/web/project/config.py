# -*- coding: utf-8 -*-
import os.path


def read_token_by_path(token_path):
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        return f.read()


def read_token(filename):
    home_path = os.path.expanduser('~')
    for path in [filename, os.path.join(home_path, filename)]:
        token = read_token_by_path(filename)
        if token is not None:
            return token
    return token


def get_value(environ_var, filename, default):
    return (
        os.environ.get(environ_var) or
        read_token(filename) or
        default
    )


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = get_value('SECRET_KEY', '.flask.secret_key', 'A0Zr98jyX RHH!jmN]LWX/,?RT')
    SECURITY_RECOVERABLE = True
    SECURITY_PASSWORD_SALT = 'sha512_crypt'
    # SECURITY_PASSWORD_SALT = 'salty'


class FacebookApiConfig:
    PAGE_ACCESS_TOKEN = get_value('FB_PAGE_ACCESS_TOKEN', '.fb.page_access_token', 'EAAraUOWW90oBABRZAGHM6X1jWIDVSQZBt7a7C6MPCuh42zk93l0LmvtMGGO0msOPrmerlANAPt0BQUZApFiiHxZCOV0ta83sFJ8J0TchhJq04nC60WrwZAFjedZB7Smj8Vo0z9Km5BTsqwYGEl3FYKYMPfkT1f0zg97e9Q9HKo4QZDZD')
    VERIFY_TOKEN = get_value('FB_VERIFY_TOKEN', '.fb.verify_token', 'verify-pipe-maria-bot')


class ApiConfig:
    AUTH_TOKEN = get_value('API_AUTH_TOKEN', '.api.auth_token', 'fedor-fedor-ay-lyu-lyu')
