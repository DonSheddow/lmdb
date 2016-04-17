import os.path
from flask import Flask

app = Flask(__name__)

DEBUG = True
FILM_DIR = os.path.expanduser("~/Videos")
IMAGE_DIR = app.static_folder + '/images'

app.config.from_object(__name__)
app.config.from_envvar('LMDB_SETTINGS', silent=True)

import lmdb.views
