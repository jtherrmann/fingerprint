import json

import flask

from . import app
from . import database


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    headers = request_headers(
        'User-Agent',
        'Accept',
        'Accept-Language',
        'Accept-Encoding',
        'DNT',
        'Upgrade-Insecure-Requests'
    )
    database.add_initial_request_fingerprint(headers)
    return flask.render_template('fingerprint.html', headers=headers)


@app.route('/fingerprint-js', methods=['POST'])
def fingerprint_js():
    headers = request_headers(
        'User-Agent', 'Accept-Language', 'Accept-Encoding', 'DNT'
    )
    other_data = json.loads(flask.request.form['fingerprint'])
    database.add_javascript_fingerprint(headers, other_data)
    return flask.jsonify(requestHeaders=headers, otherData=other_data)


def request_headers(*headers):
    return [(header, flask.request.headers[header]) for header in headers]
