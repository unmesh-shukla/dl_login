from app import app
import keras


class Facenet:

    def load_facenet(self):

        model_file_loc = app.config['MODEL_PATH']
        model = keras.models.load_model(model_file_loc, compile=False)

        return model
