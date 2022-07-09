from time import sleep
from numbers import Number
import RPi.GPIO as io

class ServoTank:
    dir_strs = {
        'back':   (-1, -1),
        'fwd':   (1, 1),
        'right':   (1, -1),
        'left':   (-1, 1),
        'stop':   (0,  0)
    }

    def __init__(self, left_pin, right_pin, freq=50, initial_value=0):
        io.setmode(io.BOARD)
        io.setup(left_pin, io.OUT)
        io.setup(right_pin, io.OUT)
        self.l = io.PWM(left_pin, freq)
        self.r = io.PWM(right_pin, freq)
        self.servos_ = (self.l, self.r)
        for pwm in self.servos_:
            pwm.start(initial_value)

    def __del__(self):
        self.kill()
        io.cleanup()

    def __getattr__(self, name):
        if name in self.dir_strs:
            l, r = self.dir_strs[name]
            def func(speed=1, time=0):
                self.set(l * speed, r * speed)
                if time:
                    sleep(time)
                    self.brake()
            return func

    def set(self, speed_l, speed_r):
        lbrake = int(speed_l != 0) 
        rbrake = int(speed_r != 0) 
        self.l.ChangeDutyCycle(lbrake * (7.5 + speed_l))
        self.r.ChangeDutyCycle(rbrake * (7.5 - speed_r))
    
    def kill(self):
        for pwm in self.servos_:
            pwm.stop()

class Coord:
    def __init__(self, *pos, time=0):
        self.pos = pos
        self.time = time 

class CoordMove:
    def __init__(self, pins, coords, freq=50):
        io.setmode(io.BOARD)
        if isinstance(pins, Number):
            pins = tuple([pins])
        self.servos_ = []
        for pin in pins:
            io.setup(pin, io.OUT)
            self.servos_.append(io.PWM(pin, freq))
            self.servos_[-1].start(0)
        self.coords = coords

        methods = dir(self)
        for coord in self.coords:
            if coord in methods:
                raise Exception(f'Invalid coord name "{coord}".') 
    
    def __del__(self):
        self.kill()
        io.cleanup()

    def __getattr__(self, name):
        return lambda: self.set(name)
    
    def set(self, coord:Coord):
        if coord not in self.coords:
            raise Exception(f'Coord {coord} not found.')
        coord = self.coords[coord]        
        
        for index, pos in enumerate(coord.pos):
            self.servos_[index].ChangeDutyCycle(pos)
        if coord.time:
            sleep(coord.time)
            self.servos_[index].ChangeDutyCycle(0)

    def brake(self):
        for pwm in self.servos_:
            pwm.ChangeDutyCycle(0)

    def kill(self):
        for pwm in self.servos_:
            pwm.stop()