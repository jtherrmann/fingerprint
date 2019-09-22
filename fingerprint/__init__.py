from flask import Flask

app = Flask(__name__)

from . import routes  # noqa: E402 F401
