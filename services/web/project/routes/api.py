# -*- coding: utf-8 -*-
from flask import Blueprint, request
from project.common import app, db
from project.config import ApiConfig


api = Blueprint('api', __name__)


@api.route('/bot/api/check')
def check():
    if request.args.get('auth_token') != ApiConfig.AUTH_TOKEN:
        return 'error'
    return 'ok'
