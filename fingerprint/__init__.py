from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fingerprint')
def fingerprint():
    return 'TODO: your fingerprint here'
