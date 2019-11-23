import base64
import json
import os
from datetime import datetime, timedelta

import flask

from . import app
from . import database
from . import util


USER_ID_KEY = 'user-id'


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/stats')
def stats():
    initial_request_stats, initial_request_total, initial_request_unique =\
        database.get_stats(database.InitialRequestFingerprint)

    js_stats, js_total, js_unique =\
        database.get_stats(database.JavaScriptFingerprint)

    return flask.render_template(
        'stats.html',

        initial_request_stats=initial_request_stats,
        initial_request_total=initial_request_total,
        initial_request_unique=initial_request_unique,

        js_stats=js_stats,
        js_total=js_total,
        js_unique=js_unique,

        format_database_column_name=util.format_database_column_name,
        get_percentage=util.get_percentage
    )


@app.route('/fingerprint')
def fingerprint():
    collection_datetime = datetime.utcnow()

    response = flask.make_response()

    user_id = flask.request.cookies.get(USER_ID_KEY)
    if user_id is None:
        user_id = new_user_id()

        max_age = 365 * 24 * 3600
        expires = datetime.utcnow() + timedelta(days=365)

        response.set_cookie(
            USER_ID_KEY, user_id, max_age=max_age, expires=expires
        )

    headers = request_headers(
        'User-Agent',
        'Accept',
        'Accept-Language',
        'Accept-Encoding',
        'DNT',
        'Upgrade-Insecure-Requests'
    )
    results = database.add_fingerprint(
        database.InitialRequestFingerprint,
        user_id,
        collection_datetime,
        headers
    )

    response.set_data(
        flask.render_template(
            'fingerprint.html',
            **results
        )
    )
    return response


def new_user_id():
    user_id = base64.b64encode(os.urandom(18)).decode()
    assert not database.cookie_id_already_exists(user_id), \
        f"cookie ID '{user_id}' already exists (this should never happen)"
    return user_id


@app.route('/fingerprint-js', methods=['POST'])
def fingerprint_js():
    collection_datetime = datetime.utcnow()
    user_id = flask.request.cookies.get(USER_ID_KEY)
    headers = request_headers(
        'User-Agent', 'Accept-Language', 'Accept-Encoding', 'DNT'
    )
    other_data = json.loads(flask.request.form['fingerprint'])
    results = database.add_fingerprint(
        database.JavaScriptFingerprint,
        user_id,
        collection_datetime,
        headers,
        js_data=other_data
    )
    return flask.jsonify(**results)


def request_headers(*headers):
    return [(header, flask.request.headers.get(header)) for header in headers]
