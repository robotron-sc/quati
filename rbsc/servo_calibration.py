from rbsc.movement import *
from rbsc.config import *

mv = ServoTank(6,13)

def grab():

    storage.storage_down()
    claw_grab.claw_open()
    sleep(1)
    storage.brake()
    claw_grab.brake()
    claw_arm.claw_down()
    sleep(1)
    claw_arm.brake()
    mv.fwd(.3)
    sleep(1)
    claw_grab.claw_close()
    mv.stop()
    sleep(.5)
    claw_arm.claw_up()
    sleep(1)
    claw_arm.brake()
    claw_grab.open_alive()
    claw_grab.brake()
