from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template('fingerprint.html')


@app.route('/results')
def results():
    return render_template(
        'results.html',
        header_user_agent=request.headers['User-Agent'],
        header_accept=request.headers['Accept']
    )
