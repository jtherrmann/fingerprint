import base64
import json
import os
from datetime import datetime, timedelta

import flask

from . import app
from . import database


USER_ID_KEY = 'user-id'


@app.route('/')
def home():
    return flask.render_template('home.html')


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
    database.add_fingerprint(
        database.InitialRequestFingerprint,
        user_id,
        collection_datetime,
        headers
    )

    response.set_data(
        flask.render_template('fingerprint.html', headers=headers)
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
    database.add_fingerprint(
        database.JavaScriptFingerprint,
        user_id,
        collection_datetime,
        headers,
        js_data=other_data
    )
    return flask.jsonify(requestHeaders=headers, otherData=other_data)


def request_headers(*headers):
    return [(header, flask.request.headers[header]) for header in headers]
