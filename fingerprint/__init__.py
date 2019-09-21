from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template(
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
    data = request.form.to_dict()
    return jsonify(
        requestHeaders=request_headers(
            'User-Agent', 'Accept-Language', 'Accept-Encoding', 'DNT'
        ),
        otherData={
            'Timezone offset': data['timezoneOffset']
        }
    )


def request_headers(*headers):
    return {header: request.headers[header] for header in headers}
