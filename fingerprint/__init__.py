from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template(
        'fingerprint.html',
        header_user_agent=request.headers['User-Agent']
    )


@app.route('/fingerprint-js', methods=['POST'])
def fingerprint_js():
    data = request.form.to_dict()
    return jsonify(
        timezoneOffset=data['timezoneOffset']
    )
