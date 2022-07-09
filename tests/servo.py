from testing import TestRoutine
from gpiozero import Servo
from time import sleep

@TestRoutine(use_execution_args=True)
def test(pins):
    servos = [Servo(int(pin)) for pin in pins]
    test_vals = [-1, 0, 1]

    for val in test_vals:
        for servo in servos:
            servo.value = val
        sleep(3)

test()