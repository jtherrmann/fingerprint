import sys

print(f'Running Python version {sys.version_info}')
assert sys.version_info >= (3, 7, 3)

import flask  # noqa: E402

app = flask.Flask(__name__)

from . import routes  # noqa: E402 F401
