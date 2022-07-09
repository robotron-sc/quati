import cv2
from sys import argv
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
from flask import Flask, render_template, Response
from rbsc.camera import Image as img

app = Flask(__name__)

def generator():
    for frame in camera.capture_continuous:
        _, jpeg = cv2.imencode('.jpg', frame.array)
        bframe = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bframe + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)