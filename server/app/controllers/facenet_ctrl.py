import logging
import os
import cv2
import base64
import numpy as np
import tensorflow as tf
from app import app, db
from app import graph, sess
from app.models.User import User
from keras.backend import set_session
import random

class FacenetController:

    def __init__(self):
        set_session(sess)


    def img_to_encoding(self, path):

        embedding = None
        img1 = cv2.imread(path, 1)
        img = img1[...,::-1]
        dim = (160, 160)

        # Comment for non-face extraction
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 1 or len(faces) == 0:
            return None

        # face = faces[0]
        # x, y, w, h = face
        # img = img[y:y+h, x:x+w]

        if(img.shape != (160, 160, 3)):
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        x_train = np.array([img])

        with graph.as_default():
            embedding = app.config['MODEL'].predict(x_train)

        return embedding


    def save_user(self, username, img_data):

        with open('images/' + username + '.jpg', "wb") as fh:
            fh.write(base64.b64decode(img_data[22:]))

        path = 'images/' + username + '.jpg'

        min_dist, identity = self.identify(path)

        if min_dist < app.config['RELAXATION_PARAM']:
            if os.path.exists(path):
                os.remove(path)
            app.logger.info("User already in the database.")
            return {
                "status": 409,
                "message": "User already in the database."
            }

        with graph.as_default():

            set_session(sess)
            encoding = self.img_to_encoding(path).tostring()

            if os.path.exists(path):
                os.remove(path)

            if encoding is None:
                identity = 0
                return {
                    "status": 400,
                    "message": "No faces found!"
                }

            try:
                user = User(username=username, encoding=encoding)
                db.session.add(user)
                db.session.commit()
                return {
                    "status": 200,
                    "message": "User added."
                }
            except:
                app.logger.info("This username has already been taken!")
                return {
                    "status": 409,
                    "message": "This username has already been taken!"
                }
        
        app.logger.critical("An internal error occurred.")
        return {
            "status": 500,
            "message": "An internal error occurred."
        }


    def identify(self, image_path):
        identity = 0
        min_dist = 1000

        encoding = self.img_to_encoding(image_path)

        if encoding is None:
            identity = 0
            return min_dist, identity

        users = User.query.all()

        for user in users:
            name = user.username
            db_enc = np.fromstring(user.encoding, dtype='float32')
            dist = np.linalg.norm(encoding - db_enc)

            if dist < min_dist:
                min_dist = dist
                identity = name

        if min_dist > app.config['RELAXATION_PARAM']:
            app.logger.info(min_dist)
            identity = 0
            app.logger.info("User not in the database.")
        else:
            app.logger.info("User -> " + str(identity) + ", Distance with Registered User " + str(min_dist))

        return min_dist, identity


    def check_user(self, img_name, img_data):
        with open('images/' + img_name + '.jpg', "wb") as fh:
            fh.write(base64.b64decode(img_data[22:]))
        path = 'images/' + img_name + '.jpg'

        with graph.as_default():
            set_session(sess)
            min_dist, identity = self.identify(path)

        if os.path.exists(path):
            os.remove(path)

        return min_dist, identity
