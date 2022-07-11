from time import sleep
from datetime import datetime
from picamera.array import PiRGBArray 
from picamera import PiCamera

from rbsc.camera import Image as img, Color
from follower import Follower

DATETIME = str(datetime.now()).replace(':', '_')
del datetime

camera = PiCamera(resolution=(640, 480), framerate=60)

STYLE = {
    'color':Color.red,
    'org': tuple(ii // 2 for ii in camera.resolution),
    'scale': 1,
    'thickness': 2
}

raw = PiRGBArray(camera, size=camera.resolution)
recorder = img.video_write(f'registers/{DATETIME}.avi', (640, 960), framerate=1)

# follower.setup

sleep(.5)
print('working.')

capture_config = {'format':'bgr', 'use_video_port':True}
follower = Follower(camera.resolution, (33, 31))
# follower.kill()

cnt = 0
macro = None
try:
    for frame in camera.capture_continuous(raw, **capture_config): 
        frdata = img.Data(frame.array)
        contrast = img.Data(frdata.contrast(1, 0))
        linedata = contrast.filter([0]*3, [255, 255, 70])
        greendata = frdata.filter([70, 200, 40], [90, 255, 100])
        
        if macro:
            cnt += 1
            if not macro(linedata, cnt):
                macro = False
        else:
            cnt = 0
            track, macro = follower.track(linedata, greendata)

        linedata.draw_label(track, org = frdata.center, thickness=2, color=Color.green)

        board = img.vboard(linedata.frame, greendata.frame)
        recorder.write(board)
        raw.truncate(0)
        sleep(.01)

except KeyboardInterrupt:
    recorder.release()
    camera.close()