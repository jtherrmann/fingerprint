import flask

from . import app


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return flask.render_template(
        'fingerprint.html',
        headers=request_headers(
            'User-Agent',
            'Accept',
            'Accept-Language',
            'Accept-Encoding',
            'DNT',
            'Upgrade-Insecure-Requests'
        )
    )


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
