#!/usr/bin/env python
from flask import Flask, Response, request, g
from flask_cors import CORS
from camera_opencv import Camera
import cv2
import sqlite3
import pandas as pd

global indexAddCounter
global currentVideoName
indexAddCounter = False
currentVideoName = ""

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

database_path = './optimodb.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_rows_from_table(query_string):
    d = {}
    table = query_db(query_string)
    # initialize columns
    for row in table:
        row_columns = row.keys()
        break
    for col in row_columns:
        d[col] = []

    for row in table:
        for col in row_columns:
            d[col].append(row[col])
    df = pd.DataFrame(d)

    return df

@app.before_request
def before_request():
    g.db=get_db()

def insertVideoInfo(id, start, end, label, imgUrl):
    sql = "insert into videoInfo values (?, ?, ?, ?, ?)"
    conn = g.db
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id, start, end, label, imgUrl))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise TypeError("insert error:{}".format(e)) #抛出异常
    return "Test3333"


def gen(camera):
    """Video streaming generator function."""
    print("step3**********************************")
    cnt = 0
    setupOutput = False
    out_started = False
    global indexAddCounter
    global currentVideoName

    while True:
        cnt += 1
        frame = camera.get_frame()
        if indexAddCounter:
            if not setupOutput:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                print("HHHHHHHHHHHHHH this is the current name: ", currentVideoName)
                print("HHHHHHHHHHHHHH video_fps: ", camera.video_fps)
                print("HHHHHHHHHHHHHH video_size: ", camera.video_size)
                try: 
                    out = cv2.VideoWriter(currentVideoName, cv2.VideoWriter_fourcc('H','2','6','4'), camera.video_fps, camera.video_size)
                except:
                    out = cv2.VideoWriter(currentVideoName, cv2.VideoWriter_fourcc(*"mp4v"), camera.video_fps, camera.video_size)
                setupOutput = True
                out_started = True
            # # print(cnt)
            # print("test1111111111111")
            out.write(frame)
        else:
            setupOutput = False
            if out_started:
                out.release()

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/streaming')
def streaming():
    print("Start streaming*********")
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/startRecord', methods=['GET', 'POST'])
def startRecord():
    global indexAddCounter
    global currentVideoName
    if request.method == 'GET':
        print("this is get method")
    else:
        content = request.get_json()
        indexAddCounter = content['startRecord']
        currentVideoName = content['videoName']
        currentVideoName = "../../Data/" + currentVideoName
        print("The recording status: ", indexAddCounter)
        print("Video name from frontend: ", currentVideoName)
    return "test"

@app.route('/stopRecord', methods=['GET', 'POST'])
def stopRecord():
    global indexAddCounter
    if request.method == 'GET':
        print("this is get method")
    else:
        content = request.get_json()
        indexAddCounter = content['stopRecord']
        # print("The recording status: ", indexAddCounter)
        # query_string = 'select label from videoInfo where id=2'
        # # df = get_rows_from_table(query_string)
        # table = query_db(query_string)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(table)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@")
        # id = "3"
        # start = "test"
        # end = "test"
        # label = "test2"
        # imgUrl = "t1111111"
        # rtn = insertVideoInfo(id, start, end, label, imgUrl)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(rtn)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@")
    return "test" 

if __name__ == '__main__':
    print("Start flask*************")
    app.run(host='0.0.0.0', debug=True, threaded=True)
