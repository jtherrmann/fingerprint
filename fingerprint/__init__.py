from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template(
        'fingerprint.html',
        headers={
            header: request.headers[header] for header in [
                'User-Agent',
                'Accept',
                'Accept-Language',
                'Accept-Encoding',
                'DNT',
                'Upgrade-Insecure-Requests'
            ]
        }
    )


@app.route('/fingerprint-js', methods=['POST'])
def fingerprint_js():
    data = request.form.to_dict()
    return jsonify(
        timezoneOffset=data['timezoneOffset']
    )
