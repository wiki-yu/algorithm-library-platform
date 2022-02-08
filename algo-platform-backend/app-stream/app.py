import os
from cv2 import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from scipy.stats import mode
import pandas as pd

from flask import Flask, Response, request, g
from flask_cors import CORS
from camera_opencv import Camera
import time


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


    
def gen(camera):
    """Video streaming generator function."""  
    cnt = 0
    start_time = time.time()

    while True:
        frame = camera.get_frame()
        # # Perform inference
        # # frame = yolov5.predict(frame)
        # # # Ref: https://news.machinelearning.sg/posts/object_detection_with_yolov5/
        # # frame.render()
        # # frame = cv2.imencode('.jpg', frame.imgs[0])[1].tobytes()

        # Initialize variables for the model
        hist_count = 7  # take into account the previous 7 frames
        data_temporal = (
            np.zeros(hist_count * 1024).astype(int).tolist()
        )  
        data_temporal = np.array([data_temporal])

        image = cv2.resize(frame, (128, 128))
        image = img_to_array(image)
        data = []
        data.append(image)
        data = np.array(data, dtype="float32") / 255.0

        # opencv images are BGR, translate to RGB
        intermediate_test_output = intermediate_layer_model.predict(data)
        data_temporal = data_temporal[0].tolist()
        data_temporal = data_temporal[len(intermediate_test_output[0]) :]
        data_temporal.extend(intermediate_test_output[0])
        data_temporal = np.array([data_temporal])
        ypredNum = xgbmodel.predict(data_temporal)
        pred_cls = class_names[int(ypredNum)]
        cnt += 1
        current_time = time.time()
        fps = cnt / (current_time - start_time) 
        txt = "Class: " + pred_cls + ' ' + "FPS: " + "{:.2f}".format(fps)
        cv2.putText(frame, txt, (0, 100), font, .5, (255, 255, 255), 1)  # text,coor
        
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
    model_path = './trained_models'
    classes_id_path = os.path.join(model_path, "classes.txt")
    classfile = open(classes_id_path, "r")
    class_names = [line[:-1] for line in classfile.readlines()]
    class_names =  ['away', 'clean_tray', 'count_pills', 'drawer', 'scan_papers_computer']

    dense_net_model_path = os.path.join(model_path, "denseXgB_model_myLayer.h5")
    xgb_model_path = os.path.join(model_path, "recognition_xgboost_prev_frames.joblib")
    intermediate_layer_model = load_model(dense_net_model_path)
    xgbmodel = load(xgb_model_path)  

    font = cv2.FONT_HERSHEY_COMPLEX

    app.run(host='0.0.0.0', debug=True, threaded=True)
