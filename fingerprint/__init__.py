from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template('fingerprint.html')


@app.route('/fingerprint-js', methods=['POST'])
def fingerprint_js():
    return jsonify(
        header_user_agent=request.headers['User-Agent']
    )


@app.route('/fingerprint-noscript')
def fingerprint_noscript():
    return render_template(
        'fingerprint-noscript.html',
        header_user_agent=request.headers['User-Agent']
    )
