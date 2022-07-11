import cv2 as cv
from rbsc.camera import Image as img, Color
from time import sleep
import VL53L0X as vl
import numpy as np

range = ((25,50,25), (140,255,140))
cam = cv.VideoCapture(0)

class TOF:
    def __init__(self):
        self.tof = vl.VL53L0X(i2c_bus=1, i2c_address=0x29)
        self.tof.open()
        self.tof.start_ranging(vl.Vl53l0xAccuracyMode.BETTER)  
        self.timing = self.tof.get_timing()
        if self.timing < 20000:
            self.timing = 20000     
        

    def check_obstacle(self):
        try:
            while True:
                distance = self.tof.get_distance()
                print(distance)

                if distance < 100:
                    _, frame = cam.read()
                    if frame is not None:
                        image = img.Data(frame)
                        cropped = image((320, 200), (150, 200))
                        mask = cropped.filter(*range, bitwise=True)

                        cv.imshow("res", mask)
                        cv.waitKey(1)
                    return True

                else: 
                    return False
        except KeyboardInterrupt:
            cv.destroyAllWindows()
            cam.release()
            
sensor = TOF()

while True:
    print(sensor.check_obstacle())
    sensor.check_obstacle()
    sleep(.4)    
