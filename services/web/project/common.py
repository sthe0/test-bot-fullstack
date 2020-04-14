# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.config import FacebookApiConfig
from project.facebook_api import FacebookApi

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
fb_api = FacebookApi.from_config(FacebookApiConfig)
