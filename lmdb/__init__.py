import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

FILM_DIR = os.path.expanduser("~/Videos")
IMAGE_DIR = app.static_folder + '/images'

app.config.from_object(__name__)
if 'LMDB_SETTINGS' in os.environ:
    app.config.from_envvar('LMDB_SETTINGS')
else:
    app.config.from_pyfile('../config.conf')

if 'SQLALCHEMY_TRACK_MODIFICATIONS' not in app.config:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config['DEBUG']

db = SQLAlchemy(app)

import lmdb.models
import lmdb.views
