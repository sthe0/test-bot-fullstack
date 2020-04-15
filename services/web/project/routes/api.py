# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from functools import wraps
from project.common import app, db
from project.config import ApiConfig


api = Blueprint('api', __name__)


def check_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.args.get('auth_token') != ApiConfig.AUTH_TOKEN:
            return jsonify(error='Unauthorized')
        return f(*args, **kwargs)

    return wrapper


@api.route('/bot/api/check')
@check_token
def check():
    return 'ok'
