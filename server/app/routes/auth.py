from app import app
from app.controllers.facenet_ctrl import FacenetController
import json
import threading
from datetime import datetime
from flask import request


@app.route('/register', methods=['POST'])
def register():

    try:
        username = request.get_json()['username']
        img_data = request.get_json()['image64']

        if len(username) == 0 or len(img_data) == 0:
            app.logger.critical(resp_dict)
            return {
                "status": 400
            }

        lock = threading.Lock()
        lock.acquire()

        f_ctrl = FacenetController()
        resp_dict = f_ctrl.save_user(username, img_data)

        lock.release()

        return resp_dict

    except:

        return {
            "status": 500
        }


@app.route('/verify', methods=['POST'])
def verify():

    img_data = request.get_json()['image64']
    img_name = str(int(datetime.timestamp(datetime.now())))

    lock = threading.Lock()
    lock.acquire()
    f_ctrl = FacenetController()
    min_dist, identity = f_ctrl.check_user(img_name, img_data)

    lock.release()

    if identity == 0:
        return json.dumps({
            "identity": 0
        })
    else:
        return json.dumps({
            "identity": str(identity)
        })
