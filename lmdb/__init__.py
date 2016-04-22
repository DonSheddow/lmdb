import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DEBUG = True
FILM_DIR = os.path.expanduser("~/Videos")
IMAGE_DIR = app.static_folder + '/images'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

app.config.from_object(__name__)
app.config.from_envvar('LMDB_SETTINGS', silent=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config['DEBUG']

db = SQLAlchemy(app)

import lmdb.models
import lmdb.views
