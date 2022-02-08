#!/usr/bin/env python
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from flask import Flask, Response, request, g
from flask_cors import CORS
from camera_opencv import Camera
import time
import os


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response



def c3d(video_path, model_path):
    """
    C3D model implementation.

    Args:
        video_path (Path) : path to the video file,
        model_path (Path) : path to the model weights file,
        video_name (str) : optional name of the video,

    Returns:
        The path to the results .csv file.
    """

    # Load the model
    model = load_model(model_path)

    temporal_length = 16    # Defined in training (always the same)
    batch_length = 16   # In order to predict faster

    # Defnied in training (these values don't depend on the dataset)
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    # Start processing
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    count_temporal = 0
    count_batch = 1
    data_temporal = None
    data_batch = []
    pred_results = []
    prob_results = []

    print('start')
    start_time = time.time()

    while vid.isOpened():
        return_value, frame = vid.read()
        if not return_value:
            print('break')

            if count_batch > 1:
                pred_idxs = model.predict(x=np.array(data_batch))
                prob_results.extend(np.amax(pred_idxs, axis=1))

                # Obtain class results from predictions
                if len(pred_idxs[0]) == 1:
                    pred_idxs = np.round(pred_idxs).astype(int).flatten()
                else:
                    pred_idxs = np.argmax(pred_idxs, axis=1)
                pred_results.extend(pred_idxs)
            break

        image = cv2.resize(frame, (112, 112))
        image = image/255
        image = (image - mean) / std

        if count_temporal < temporal_length:
            if count_temporal == 0:
                data_temporal = np.array([image])
            else:
                data_temporal = np.append(data_temporal, [image], axis=0)

        if count_temporal >= temporal_length:
            data_temporal[:-1] = data_temporal[1:]
            data_temporal[-1] = image

        if count_temporal >= (temporal_length - 1):
            if count_batch < batch_length:
                if count_batch == 1:
                    data_batch = np.array([data_temporal])
                else:
                    data_batch = np.append(data_batch, [data_temporal], axis=0)
                count_batch += 1
            else:
                data_batch = np.append(data_batch, [data_temporal], axis=0)
                pred_idxs = model.predict(x=data_batch)
                prob_results.extend(np.amax(pred_idxs, axis=1))

                # Obtain class results from predictions
                if len(pred_idxs[0]) == 1:
                    pred_idxs = np.round(pred_idxs).astype(int).flatten()
                else:
                    pred_idxs = np.argmax(pred_idxs, axis=1)
                pred_results.extend(pred_idxs)
                count_batch = 1
                data_batch = []

                print('count: ', count_temporal)
        count_temporal += 1

    end_time = time.time()
    print(f'total_time: {end_time - start_time:0.3f} sec')
    vid.release()




    
def gen(camera):
    """Video streaming generator function."""

    # Load the model
    model = load_model(test_model)

    temporal_length = 16    # Defined in training (always the same)
    batch_length = 16   # In order to predict faster

    # Defnied in training (these values don't depend on the dataset)
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    count_temporal = 0
    count_batch = 1
    data_temporal = None
    data_batch = []
    pred_results = []
    prob_results = []

    while True:
        frame = camera.get_frame()
        image = cv2.resize(frame, (112, 112))
        image = image/255
        image = (image - mean) / std

        if count_temporal < temporal_length:
            if count_temporal == 0:
                data_temporal = np.array([image])
            else:
                data_temporal = np.append(data_temporal, [image], axis=0)
            continue

        if count_temporal >= temporal_length:
            data_temporal[:-1] = data_temporal[1:]
            data_temporal[-1] = image
        
        pred_idxs = model.predict(x=data_batch)
        pred_idxs = np.argmax(pred_idxs, axis=1)
        print(pred_idxs)
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
    test_model = "./models/C3D_scratch_best_optimo_v1.1.hdf5"
    app.run(host='0.0.0.0', debug=True, threaded=True)

