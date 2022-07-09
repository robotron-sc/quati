from time import sleep
from flask import Flask, render_template, Response
from picamera.array import PiRGBArray 
from picamera import PiCamera
# Personal files 
import follower
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
    follower.setup(camera.resolution)
    follower.kill()
    
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = img.Data(frame.array)

        if image is None:
            continue 

        label= follower.track(image)

        image.draw_label(label, **STYLE)

        raw_capture.truncate(0)
        
        # display = img.Data(img.vboard(image.frame, green.frame))
        # print(green.shape, image.shape)
        byteframe = bytes(image)
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