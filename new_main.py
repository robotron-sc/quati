from time import sleep
from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera

from rbsc.camera import Image as img, Color
import new_follower as follower

DATETIME = str(datetime.now()).replace(':', '_')
del datetime

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60

raw = PiRGBArray(camera, size=(640, 480))
recorder = img.video_write(f'registers/{DATETIME}.avi', camera.resolution, framerate=10)

follower.setup(camera.resolution, 33, 31)

sleep(.8)
print('working...')

macro = None
try:
    for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
        image = img.Data(frame.array)
        contrast = img.Data(image.contrast(1, 0))
        filtered = contrast.filter([0]*3, [255, 255, 100])

        if macro:
            if not macro(filtered):
                macro = False
        else:
            label, macro = follower.track(filtered)
        
        filtered.draw_label(
            label,
            color=Color.green,
            org=image.center,
            scale=2
        )
        print(label)

        recorder.write(filtered.frame)
        raw.truncate(0)
        sleep(.1)
except KeyboardInterrupt:
    recorder.release()
    follower.kill()
    camera.close()