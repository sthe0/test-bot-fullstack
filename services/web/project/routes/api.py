# -*- coding: utf-8 -*-
from flask import Blueprint, request
from project.common import app, db


SECRET_TOKEN = 'fedor-fedor-ay-lyu-lyu'


api = Blueprint('api', __name__)


@api.route('/bot/api/check')
def check():
    if request.args.get('auth_token') != SECRET_TOKEN:
        return 'error'
    return 'ok'
