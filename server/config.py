import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MODEL_PATH = base_dir + '/app/models/model_files/facenet_keras.h5'
    MODEL = None
    RELAXATION_PARAM = 6

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            "sqlite:///" + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False