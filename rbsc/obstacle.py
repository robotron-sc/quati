import cv2 as cv
from cv2 import threshold
from camera import Image as img, Color
from time import sleep
import VL53L0X as vl
from config import *
from movement import ServoTank

low_blue= [105,50,0]
high_blue=[135, 255, 255]
rang = [(135, 175), (50, 255), (0, 110)]
cam = cv.VideoCapture(0)

mv = ServoTank(33, 31)

class TOF:
    def __init__(self):
        self.tof=vl.VL53L0X(i2c_bus=1, i2c_address=0x29)
        self.tof.open()
        self.tof.start_ranging(vl.Vl53l0xAccuracyMode.BETTER)
        self.timing = self.tof.get_timing()
        if self.timing < 20000:
            self.timing = 20000

    def check_obstacle(self):
        try:

            distance=self.tof.get_distance()
            print(distance)

            if distance < 100:
                _,frame = cam.read()
                image=img.Data(frame)
                cropped = image((320,300),(250,300))
                hsv=cropped.hsv
                gray=cropped.grayscale
                blur=cropped.blur((3,3))
                blue_filter = cropped.filter(*(low_blue, high_blue), colors=([255]*3,[0]*3), bitwise=False)
                # edges = cv.Canny(blue_filter, threshold1=150, threshold2=205)
                # contours, hierarquy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                # cv.drawContours(cropped.frame, contours, -1, (0,255,0),3)
                blue_filter.save(name="objeto",path="rbsc/png")                
                color = cropped.dominant_colors(1)[0] 
                check = [x in range(*rang[i]) for i, x in enumerate(color)]
                print(all(check))
                print(check)
                print(color)
                return not all(check)
            else:
                return None
        except KeyboardInterrupt:
            cv.destroyAllWindows()
            cam.release()

sensor = TOF()

while True:
    obs = sensor.check_obstacle()
    if obs is not None:
        if obs:
            print("Obstáculo")

        else:
            print("Kit")
            storage.storage_down()
            sleep(.5)
            storage.brake()
            sleep(.5)
            claw_grab.claw_open()
            sleep(.5)
            claw_arm.claw_down()
            sleep(.5)
            mv.fwd(.3)
            sleep(1)
            mv.stop()
            sleep(.5)
            claw_grab.claw_close()
            sleep(.5)
            claw_grab.brake()
            sleep(.5)
            claw_arm.claw_up()
            sleep(1)
            claw_arm.brake()
            sleep(1)
            claw_grab.open_alive()
            claw_grab.brake()
            sleep(.5)


    sleep(1)