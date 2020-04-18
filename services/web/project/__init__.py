# -*- coding: utf-8 -*-
from flask import jsonify, request
from project.common import app, db
from project.routes import facebook, api
from project.security import security, user_datastore, login_required


app.register_blueprint(api)
app.register_blueprint(facebook)


@app.before_first_request
def create_user():
    # db.drop_all()
    # db.create_all()
    # user_datastore.create_user(email='admin@fedor-solovyev.ru', password='P@ssw0rd@')
    db.session.commit()


@app.route('/say_again')
def say_again():
    return jsonify({
        'you said:': request.args.get('text')
    })


@app.route('/test')
def test():
    return jsonify(hello='test')


@app.route('/')
def home():
    return jsonify(hello='home')


@app.route('/other')
@login_required
def other():
    return jsonify(hello='other')
