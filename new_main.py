from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera

from rbsc.camera import Image as img
import follower

DATETIME = str(datetime.now()).replace(':', '_')
del datetime

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60

raw = PiRGBArray(camera, size=(640, 480))
recorder = img.video_write(f'registers/{DATETIME}.avi', camera.resolution, framerate=10)

follower(camera.resolution)
sleep(.5)
print('working...')

scope = None
try:
    for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
        image = img.Data(frame.array)
        if macro:
            if not macro(image):
                macro = False
        else:
            label, macro = new_follower.track(image)
        
        # image.draw_label(label, **STYLE)
        print(label)

        recorder.write(frame.array)
        raw.truncate(0)
        sleep(.1)
except KeyboardInterrupt:
    register.release()
    follower.kill()
    camera.close()