from config import Config
from flask import Flask
from flask_cors import CORS
import tensorflow as tf
import keras
from keras.backend import set_session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging


graph = tf.get_default_graph()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

sess = tf.Session()
set_session(sess)

from app.models.facenet import Facenet
if app.config['MODEL'] is None:
    app.config['MODEL'] = Facenet().load_facenet()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app import routes
from app.routes import auth


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
