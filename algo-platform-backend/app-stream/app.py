#!/usr/bin/env python
from flask import Flask, Response, request, g
from flask_cors import CORS
from camera_opencv import Camera
import cv2
import pandas as pd
from yolov5 import YOLOv5, detect
from yolov5.utils.torch_utils import select_device


global indexAddCounter
global currentVideoName
indexAddCounter = False
currentVideoName = ""

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

device = '' # "0" or "cpu"
device = select_device(device)

# Init YOLOv5 model
yolov5 = YOLOv5("./models/yolov5s.pt", device=device)


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        # Perform inference
        # frame = yolov5.predict(frame)
        # # Ref: https://news.machinelearning.sg/posts/object_detection_with_yolov5/
        # frame.render()
        # frame = cv2.imencode('.jpg', frame.imgs[0])[1].tobytes()

        
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
