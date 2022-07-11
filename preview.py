from time import sleep
from flask import Flask, render_template, Response
from picamera.array import PiRGBArray 
from picamera import PiCamera
# Personal files 
from follower import Follower
from rbsc.camera import Image as img, Color
 
stream = Flask(__name__)
STYLE = {
    'color':Color.red,
    'org':(320, 240),
    'scale': 1,
    'thickness': 2
}

def generator():
    camera = PiCamera(resolution=(640, 480), framerate=60)
    raw = PiRGBArray(camera, size=camera.resolution)

    sleep(.5)
    print('working.')

    capture_config = {'format':'bgr', 'use_video_port':True}
    follower = Follower(camera.resolution, (33, 31))
    follower.kill()

    for frame in camera.capture_continuous(raw, **capture_config): 
        frdata = img.Data(frame.array)
        contrast = img.Data(frdata.contrast(.9, 0))
        frdata = contrast.filter([0]*3, [255, 255, 130])

        track = follower.track(frdata)
        frdata.draw_label(track, org = frdata.center, thickness=2, color=Color.green)

        byteframe = bytes(frdata)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + byteframe + b'\r\n\r\n')
        raw.truncate(0)
        sleep(.01)

@stream.route('/')
def index():
    return render_template('index.html')

@stream.route('/video_feed')
def video_feed():
    return Response(generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    stream.run(host='0.0.0.0', port='5001', debug=True)