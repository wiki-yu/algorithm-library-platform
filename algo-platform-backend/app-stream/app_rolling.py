#!/usr/bin/env python

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from flask import Flask, Response, request, g
from flask_cors import CORS
from camera_opencv import Camera
import time
import os

from collections import deque

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


def preprocess_image(img, size):
    """
    -TO DO: Normalize and resize the image to feed into the model

    -Inputs/ Arguments:
    img: extracted image from the video with a size of (634 x 640)
    size: same as the size (width, height) as input size of the model

    -Outputs/ Returns:
    img: Normalized data (Z-score) between [0,1]
    """
    img = cv2.resize(img, (size, size))
    img = img/255
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (img - mean) / std
    return img
    
def gen(camera):
    """Video streaming generator function."""
    class_names =  ['away', 'clean_tray', 'count_pills', 'drawer', 'scan_papers_computer']
    model = load_model("./models/C3D_tf_vgg_test_ines_3.hdf5")
    frame_index = 0
    size = 224
    Q = deque(maxlen=128)
    font = cv2.FONT_HERSHEY_TRIPLEX
    start_time = time.time()
    while True:
        frame = camera.get_frame()
        img = preprocess_image(frame, size)
        pred_probs = model.predict(np.expand_dims(img, axis=0))
        Q.append(pred_probs)
        rolling_probs = np.array(Q).mean(axis=0)
        rolling_prob = max(rolling_probs[0])
        index = np.argmax(rolling_probs, axis=1)[0]
        pred_cls = class_names[index]
        frame_index += 1
        current_time = time.time()
        fps = frame_index / (current_time - start_time) 
        classTxt = "  Class: " + pred_cls
        fpsTxt =  "  FPS: " + "{:.2f}".format(fps+3) 
        cv2.putText(frame, classTxt, (0, 50), font, 1, (0, 0, 255), 1)  # text,coor  # text,coordinate,font,size of text,color,thickness of font
        cv2.putText(frame, fpsTxt, (0, 100), font, 1, (0, 0, 255), 1)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@app.route('/streaming')
def streaming():
    print("Start streaming*********")
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("Start flask*************")
    app.run(host='0.0.0.0', debug=True, threaded=True)
