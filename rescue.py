import cv2 as cv
import numpy as np
from time import sleep
from rbsc.movement import *
from rbsc.servo_calibration import *
from rbsc.camera import *


def rescue(fr):
    gray = cv.cvtColor(fr, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (17,17), 0)

    input = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, 100,
                                param1=100, param2=20, minRadius=80, maxRadius=0)


    if input is not None:
        circles = np.uint16(np.around(input))

        print("ACHEI BOLA") 
         
        for circle in circles[0, :]:
            cv.circle(fr, (circle[0],circle[1]), circle[2], (255,0,0), 3)

        data = Image.Data(fr)
        x, y = data.center
        if circle[0] < x:
            mv.left(0.2)
            sleep(.5)
        else:
            mv.right(0.2)
            sleep(.5)

        mv.stop()
        sleep(1)
        mv.back(.3)
        sleep(0.4)
        mv.stop()
        grab()
    else: 
        mv.fwd(.3)
        