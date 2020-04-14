# -*- coding: utf-8 -*-
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "A0Zr98jyX RHH!jmN]LWX/,?RT"


class FacebookApiConfig:
    PAGE_ACCESS_TOKEN = 'EAAraUOWW90oBABRZAGHM6X1jWIDVSQZBt7a7C6MPCuh42zk93l0LmvtMGGO0msOPrmerlANAPt0BQUZApFiiHxZCOV0ta83sFJ8J0TchhJq04nC60WrwZAFjedZB7Smj8Vo0z9Km5BTsqwYGEl3FYKYMPfkT1f0zg97e9Q9HKo4QZDZD'
    VERIFY_TOKEN = 'verify-pipe-maria-bot'
