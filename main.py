from time import sleep
from datetime import datetime
from picamera.array import PiRGBArray 
from picamera import PiCamera
# Personal files 
from rbsc.camera import Image as img, Color
from rbsc.utils import empty_folder
import follower
 
DATETIME = str(datetime.now()).replace(':', '_')
del datetime
# empty_folder('registers')

STYLE = {
    'color':Color.red,
    'org':(320, 240),
    'scale': 1,
    'thickness': 2
}

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60 


raw_capture = PiRGBArray(camera, size=(640, 480))
register = img.video_write(f'registers/{DATETIME}.avi', camera.resolution, framerate=10)

follower.setup(camera.resolution)
sleep(.5)
print('working')

scope = None
try:
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = img.Data(frame.array)
        if scope:
            if not scope(image):
                scope = False
        else:
            label, scope = follower.track(image)
        
        image.draw_label(label, **STYLE)
        print(label)

        register.write(frame.array)
        raw_capture.truncate(0)
        sleep(.1)

except KeyboardInterrupt:
    camera.close()
    follower.kill()
    register.release()