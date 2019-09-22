import flask

app = flask.Flask(__name__)

from . import routes  # noqa: E402 F401
