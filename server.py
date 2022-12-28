from flask import Flask, Response
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
video = cv2.VideoCapture('/dev/video1')


def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/")
def video_feed():
    global video
    return Response(gen(video), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
