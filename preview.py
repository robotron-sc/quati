from time import sleep
from flask import Flask, render_template, Response
from picamera.array import PiRGBArray 
from picamera import PiCamera
# Personal files 
import new_follower as follower
from rbsc.camera import Image as img, Color
 
stream = Flask(__name__)
STYLE = {
    'color':Color.red,
    'org':(320, 240),
    'scale': 1,
    'thickness': 2
}

def generator():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60 
    raw_capture = PiRGBArray(camera, size=(640, 480))
    follower.setup(camera.resolution, 33, 31)
    follower.kill()
    
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = img.Data(frame.array)
        if image is None:
            continue 

        contrast = img.Data(image.contrast(1, 0))
        line = contrast.filter([0]*3, [255, 255, 100])

        label, _ = follower.track(line)

        # image.draw_label(label, **STYLE)
        line.draw_label(
            label,
            color=Color.green,
            org=image.center,
            scale=2
        )

        raw_capture.truncate(0)
        
        # display = img.Data(img.vboard(image.frame, green.frame))
        # print(green.shape, image.shape)
        byteframe = bytes(line)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byteframe + b'\r\n\r\n')

@stream.route('/')
def index():
    return render_template('index.html')

@stream.route('/video_feed')
def video_feed():
    return Response(generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    stream.run(host='0.0.0.0', port='5001', debug=True)