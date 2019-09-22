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
    data = flask.request.form.to_dict()
    return flask.jsonify(
        requestHeaders=request_headers(
            'User-Agent', 'Accept-Language', 'Accept-Encoding', 'DNT'
        ),
        otherData=[
            ('Timezone offset', data['timezoneOffset'])
        ]
    )


def request_headers(*headers):
    return [(header, flask.request.headers[header]) for header in headers]
